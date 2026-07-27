from pathlib import Path
import joblib
import pandas as pd


class DamagePredictor:

    def __init__(self):

        root = Path(__file__).resolve().parent.parent

        model_path = root / "models" / "damage_mode_pipeline.pkl"

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        bundle = joblib.load(model_path)

        self.pipeline = bundle["pipeline"]
        self.feature_names = bundle["feature_names"]
        self.classes = bundle["classes"]

    # =====================================================

    def predict(self, features: dict):

        # Check missing features
        missing = [
            feature
            for feature in self.feature_names
            if feature not in features
        ]

        if missing:

            raise ValueError(
                f"Missing features: {missing}"
            )

        # Ignore extra features automatically
        df = pd.DataFrame([features])

        df = df[self.feature_names]

        prediction = self.pipeline.predict(df)[0]

        confidence = None

        probabilities = {}

        if hasattr(self.pipeline, "predict_proba"):

            probs = self.pipeline.predict_proba(df)[0]

            confidence = float(probs.max())

            probabilities = {
                label: round(float(prob), 4)
                for label, prob in zip(self.classes, probs)
            }

        return {
            "damage_mode": prediction,
            "confidence": round(confidence, 4) if confidence else None,
            "probabilities": probabilities
        }

    # =====================================================

    def required_features(self):

        return self.feature_names