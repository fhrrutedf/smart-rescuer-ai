"""
Test AI Models Status
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

print("=" * 60)
print("Smart Rescuer - AI Status Check")
print("=" * 60)
print()

# Test 1: TensorFlow Lite
print("1. Testing TensorFlow Lite...")
try:
    import tensorflow as tf
    print(f"   ✓ TensorFlow installed: v{tf.__version__}")
    
    try:
        import tensorflow.lite as tflite
        print("   ✓ TensorFlow Lite available")
    except:
        print("   ✗ TensorFlow Lite NOT available")
except ImportError:
    print("   ✗ TensorFlow NOT installed")
    print("   → Install with: pip install tensorflow")

print()

# Test 2: Injury Detection Model
print("2. Testing Injury Detection Model...")
try:
    from ai_engine.injury_detector import InjuryDetector
    detector = InjuryDetector()
    
    if detector.is_model_loaded:
        print("   ✓ Injury model LOADED successfully")
        print(f"   ✓ Model path: {detector.model_path}")
        print(f"   ✓ Classes: {len(detector.INJURY_CLASSES)}")
    else:
        print("   ⚠ Injury model found but NOT loaded")
        print("   → Using rule-based fallback")
except Exception as e:
    print(f"   ✗ Error loading injury model: {e}")

print()

# Test 3: Severity Scorer
print("3. Testing Severity Scorer...")
try:
    from ai_engine.severity_scorer import SeverityScorer
    scorer = SeverityScorer()
    
    # Test calculation
    test_result = scorer.calculate_score(
        vital_signs={'heart_rate': 75, 'spo2': 98, 'body_temperature': 37.0},
        injuries=[],
        patient_conscious=True
    )
    
    print(f"   ✓ Severity scorer working")
    print(f"   ✓ Test score: {test_result['total_score']:.1f}/10")
    print(f"   ✓ Level: {test_result['severity_level']}")
except Exception as e:
    print(f"   ✗ Error with severity scorer: {e}")

print()

# Test 4: Medical Chatbot
print("4. Testing Medical Chatbot...")
try:
    from ai_engine.chatbot import MedicalChatbot
    chatbot = MedicalChatbot()
    
    if chatbot.model_available:
        print("   ✓ Chatbot model available")
        print(f"   ✓ Model: {chatbot.model_name}")
    else:
        print("   ⚠ Chatbot using rule-based responses")
        print("   → Ollama not available")
except Exception as e:
    print(f"   ✗ Error with chatbot: {e}")

print()
print("=" * 60)
print("Summary:")
print("=" * 60)

# Check if main AI features work
ai_working = False
try:
    from ai_engine.injury_detector import InjuryDetector
    from ai_engine.severity_scorer import SeverityScorer
    
    detector = InjuryDetector()
    scorer = SeverityScorer()
    
    if detector.is_model_loaded:
        print("✓ Core AI features: WORKING (TFLite model loaded)")
        ai_working = True
    else:
        print("⚠ Core AI features: FALLBACK MODE (rule-based)")
        print("  Install TensorFlow to enable AI model:")
        print("  pip install tensorflow==2.15.0")
except Exception as e:
    print(f"✗ Core AI features: ERROR - {e}")

print("=" * 60)
