import tensorflow as tf

# Wyświetla listę dostępnych urządzeń fizycznych (GPU i CPU)
gpus = tf.config.list_physical_devices('GPU')
cpus = tf.config.list_physical_devices('CPU')

print("Dostępne urządzenia GPU:", gpus)
print("Dostępne urządzenia CPU:", cpus)
