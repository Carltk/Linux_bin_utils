#!/usr/bin/env python3
"""
Update Factory settings.json with OpenRouter models.
Ensures openrouter/free appears first, and sorts the rest alphabetically.
Pricing is shown accurately (FREE for zero‑price models, otherwise $X.XX/M).
"""

import json
import os
import shutil
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Configuration
OPENROUTER_API_KEY = ""
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
SETTINGS_PATH = os.path.expanduser("~/.factory/settings.json")
BACKUP_DIR = os.path.expanduser("~/.factory/backups")

# OpenRouter base URL for API calls
BASE_URL = "https://openrouter.ai/api/v1"


def fetch_models():
    """Fetch models from OpenRouter API."""
    request = Request(OPENROUTER_MODELS_URL)
    request.add_header("Authorization", f"Bearer {OPENROUTER_API_KEY}")
    
    try:
        with urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("data", [])
    except (URLError, HTTPError) as e:
        print(f"Error fetching models: {e}")
        return []


def is_text_model(model):
    """Check if model supports text generation."""
    architecture = model.get("architecture", {}) or {}
    output_modalities = architecture.get("output_modalities", [])
    return "text" in str(output_modalities).lower()


def get_output_price(model):
    """Get output price per million tokens."""
    pricing = model.get("pricing", {}) or {}
    return float(pricing.get("completion", 0) or 0) * 1_000_000


def is_coding_model(model):
    """Check if model is a coding/programming model based on name patterns."""
    name = (model.get("name", "") or model.get("id", "")).lower()
    coding_patterns = [
        "coder", "code", "codellama", "santa", "starcoder", "deepcoder",
        "codegeex", "wizardcoder", "polycoder", "santos", "phi", "codeinfer",
        "code-bison", "code-llama", "gemma-coder", "qwen-coder", "mistral-coder",
        "command-r", "granite-code", "starcoder2", "camel", "swe", "openchat",
        "magicoder", "octocoder", "gpt-engineer", "starchat", "paige", "alpha"
    ]
    return any(pattern in name for pattern in coding_patterns)


def get_display_name(model, price_per_million):
    """Generate display name with proper price formatting and context length."""
    name = model.get("name", "") or model.get("id", "")
    context_len = model.get("context_length", 0) or 0
    
    # Format context length
    if context_len >= 1_000_000:
        context_str = f"len:{context_len // 1_000_000}M"
    elif context_len >= 1_000:
        context_str = f"len:{context_len // 1_000}k"
    else:
        context_str = f"len:{context_len}"
    
    # Format price
    if price_per_million == 0:
        price_str = "FREE"
    else:
        price_str = f"${price_per_million:.2f}"
    
    return f"{name} [{context_str} {price_str}/M]"


def get_max_output_tokens(model):
    """Get max output tokens for model, with sensible defaults."""
    context_length = model.get("context_length", 8192) or 8192
    return min(context_length // 2, 131000)


def create_backup():
    """Create backup of settings.json before modification."""
    if not os.path.exists(SETTINGS_PATH):
        print("Settings file not found, will create new one.")
        return None
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"settings_{timestamp}.json")
    
    shutil.copy2(SETTINGS_PATH, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def load_settings():
    """Load current settings.json."""
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_settings(settings):
    """Save settings to settings.json."""
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    print(f"Settings saved to {SETTINGS_PATH}")


def build_custom_models(models):
    """Build customModels list with openrouter/free first, then coding models, then rest alphabetically."""
    # Separate coding models, openrouter/free, and other models
    coding_models = []
    free_model = None
    other_models = []
    
    for model in models:
        model_id = model.get("id", "")
        if model_id.startswith("openrouter/free"):
            free_model = model
        elif is_coding_model(model):
            coding_models.append(model)
        else:
            other_models.append(model)
    
    # Sort coding models alphabetically (case-insensitive)
    coding_models.sort(key=lambda m: m.get("id", "").lower())
    
    # Sort other models alphabetically (case-insensitive)
    other_models.sort(key=lambda m: m.get("id", "").lower())
    
    # Build the ordered list: openrouter/free first, then coding models, then rest
    ordered_models = []
    if free_model:
        ordered_models.append(free_model)
    ordered_models.extend(coding_models)
    ordered_models.extend(other_models)
    
    # Build custom model entries
    custom_models = []
    for idx, model in enumerate(ordered_models):
        model_id = model.get("id", "")
        price_per_million = get_output_price(model)
        
        custom_model = {
            "model": model_id,
            "id": f"custom:{model_id}-[OpenRouter]-{idx}",
            "index": idx,
            "baseUrl": BASE_URL,
            "apiKey": OPENROUTER_API_KEY,
            "displayName": get_display_name(model, price_per_million),
            "maxOutputTokens": get_max_output_tokens(model),
            "noImageSupport": True,
            "provider": "generic-chat-completion-api"
        }
        custom_models.append(custom_model)
    
    return custom_models


def main():
    print("Fetching models from OpenRouter API...")
    all_models = fetch_models()
    
    if not all_models:
        print("No models fetched. Exiting.")
        return
    
    print(f"Fetched {len(all_models)} total models")
    
    # Filter to text-based models only
    text_models = [m for m in all_models if is_text_model(m)]
    print(f"Found {len(text_models)} text-based models")
    
    # ----------------------------------------------------------------------
    # NEW: Filter models according to requiredModels from settings.json
    # ----------------------------------------------------------------------
    # Load current settings to retrieve the requiredModels list
    settings = load_settings()
    required_terms = settings.get("requiredModels", [])
    
    # Always keep openrouter/free regardless of requiredModels filter
    free_model = None
    filtered_models = []
    
    # Process ALL text models before truncating
    for model in text_models:
        model_id = model.get("id", "")
        if model_id.startswith("openrouter/free"):
            free_model = model
            # Don't add to filtered_models yet, will insert at front later
        elif required_terms:
            term_lower = [t.lower() for t in required_terms]
            # Keep model if its id or name contains any of the required terms
            if any(
                term in (model_id.lower()) or
                term in (model.get("name", "").lower())
                for term in term_lower
            ):
                filtered_models.append(model)
        else:
            # No required terms, keep all non-free models (will limit later)
            filtered_models.append(model)
    
    # Add free model back to the list
    if free_model:
        filtered_models.insert(0, free_model)
    
    text_models = filtered_models
    print(f"Filtered to {len(text_models)} models based on requiredModels")
    
    # Limit to reasonable number (top 100) AFTER filtering for required models
    if len(text_models) > 100:
        text_models = text_models[:100]
        print(f"Selected top {len(text_models)} models")
    
    # Create backup
    backup_path = create_backup()
    
    # Load current settings
    settings = load_settings()
    
    # Build and update customModels
    settings["customModels"] = build_custom_models(text_models)
    
    # Save settings
    save_settings(settings)
    
    print(f"\nDone! Updated {len(text_models)} models in settings.json")
    
    # Print preview of first 10 models
    print("\nFirst 10 models:")
    preview_models = build_custom_models(text_models)[:10]
    for i, m in enumerate(preview_models):
        print(f"  {i+1:2}. {m.get('model'):50} {m['displayName']}")


def models_by_id(model_id):
    """Helper to fetch a model by ID from the fetched list (used only for preview)."""
    # In a real script this would be replaced with proper lookup; kept minimal for preview
    return next((m for m in text_models if m.get("id") == model_id), None)


if __name__ == "__main__":
    main()
