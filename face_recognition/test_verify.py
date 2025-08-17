from deepface import DeepFace

result = DeepFace.verify("reference_2.jpg", "reference_2.jpg")
print(result)
