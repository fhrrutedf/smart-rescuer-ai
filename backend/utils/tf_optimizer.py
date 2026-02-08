"""
TensorFlow Performance Optimization
Sets environment variables and configurations for faster inference
"""
import os
import logging

# Disable TensorFlow logging (reduces overhead)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0=all, 1=info, 2=warning, 3=error

# Enable XLA (Accelerated Linear Algebra) for faster execution
os.environ.setdefault('TF_XLA_FLAGS', '--tf_xla_auto_jit=2')

# Enable oneDNN optimizations (improves CPU performance)
os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '1')

# Use fewer threads to reduce overhead (adjust based on your CPU)
os.environ.setdefault('TF_NUM_INTRAOP_THREADS', '2')
os.environ.setdefault('TF_NUM_INTEROP_THREADS', '2')

# Disable GPU growth (if you don't have GPU, this speeds up initialization)
os.environ.setdefault('TF_FORCE_GPU_ALLOW_GROWTH', 'true')

def configure_tensorflow():
    """Configure TensorFlow for optimal performance"""
    try:
        import tensorflow as tf
        
        # Set memory growth for GPU (if available)
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logging.info(f"GPU available: {len(gpus)} GPU(s) found")
        else:
            logging.info("No GPU found, using CPU")
            # Optimize CPU usage
            tf.config.threading.set_intra_op_parallelism_threads(2)
            tf.config.threading.set_inter_op_parallelism_threads(2)
        
        # Disable eager execution for faster inference (use graph mode)
        # tf.compat.v1.disable_eager_execution()  # Uncomment if using TF 1.x style
        
        logging.info("TensorFlow optimized for inference")
        return True
        
    except ImportError:
        logging.warning("TensorFlow not available")
        return False
    except Exception as e:
        logging.error(f"Error configuring TensorFlow: {e}")
        return False

# Auto-configure on import
configure_tensorflow()
