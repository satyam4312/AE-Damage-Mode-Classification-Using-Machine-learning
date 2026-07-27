"""
train.py
-------------------------------------------------------
Train Damage Mode Classification Model

Pipeline

clean_dataset.csv
        │
        ▼
Train/Test Split
        │
        ▼
Model Training
        │
        ▼
Model Evaluation
        │
        ▼
Best Model Selection
        │
        ▼
damage_mode_pipeline.pkl
"""

import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer


from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    GradientBoostingClassifier,
    ExtraTreesClassifier
)

from imblearn.ensemble import BalancedRandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from config import (
    PROCESSED_DIR,
    MODEL_DIR,
    OUTPUT_DIR,
    RANDOM_STATE,
    TEST_SIZE
)


class DamageModeTrainer:

    def __init__(self):

        self.df = pd.read_csv(PROCESSED_DIR / "clean_dataset.csv")

        if "damage_mode" not in self.df.columns:
            raise ValueError("damage_mode column not found.")

        self.X = self.df.drop(columns=["damage_mode"])

        # Keep string labels directly
        self.y = self.df["damage_mode"]

        self.models = {
        "Balanced Random Forest":
            BalancedRandomForestClassifier(
                n_estimators=150,
                max_depth=15,
                min_samples_leaf=5,
                random_state=RANDOM_STATE,
                n_jobs=-1
),

        "Extra Trees":
            ExtraTreesClassifier(
                n_estimators=150,
                class_weight="balanced",
                random_state=RANDOM_STATE,
                n_jobs=-1
            ),

        "Gradient Boosting":
            GradientBoostingClassifier(
                random_state=RANDOM_STATE
            )
        }

    # ======================================================

    def split_dataset(self):

        (self.X_train, self.X_test, self.y_train, self.y_test) = train_test_split(
            self.X,
            self.y,
            test_size = TEST_SIZE,
            stratify = self.y,
            random_state = RANDOM_STATE
        )

        self.feature_names = self.X.columns.tolist()
        
    # ======================================================

    def build_pipeline(self, classifier):

        pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy = "median")),
            ("classifier", classifier)
        ])

        return pipeline

    # ======================================================

    def evaluate(self, model):

        prediction = model.predict(self.X_test)

        metrics = {
            "Accuracy" : accuracy_score(self.y_test, prediction),

            "Precision" : precision_score(self.y_test, prediction, average="weighted"),

            "Recall" : recall_score(self.y_test, prediction, average="weighted"),

            "F1" : f1_score(self.y_test, prediction, average="weighted")
        }

        return metrics, prediction

    # ======================================================

    def train_models(self):

        results = []

        best_f1 = 0

        for name, classifier in self.models.items():

            print("=" * 60)
            print(f"Training : {name}")

            pipeline = self.build_pipeline(classifier)

            pipeline.fit(self.X_train, self.y_train)

            metrics, prediction = self.evaluate(pipeline)

            print(classification_report(self.y_test, prediction, digits = 4, zero_division = 0))

            results.append({
                "Model": name, **metrics
            })

            if metrics["F1"] > best_f1:

                best_f1 = metrics["F1"]

                self.best_pipeline = pipeline

                self.best_metrics = metrics

                self.best_prediction = prediction

                self.best_name = name

        self.results = pd.DataFrame(results)

    # ======================================================

    def save_model(self):

        model_bundle = {
        "pipeline": self.best_pipeline,
        "feature_names": self.feature_names,
        "classes": self.best_pipeline.classes_
        }

        joblib.dump(model_bundle, MODEL_DIR / "damage_mode_pipeline.pkl")

        self.results.to_csv(OUTPUT_DIR / "metrics.csv", index=False)

        summary = {
        "best_model": self.best_name,
        "accuracy": float(self.best_metrics["Accuracy"]),
        "precision": float(self.best_metrics["Precision"]),
        "recall": float(self.best_metrics["Recall"]),
        "f1": float(self.best_metrics["F1"])
        }

        with open(OUTPUT_DIR / "training_summary.json", "w") as f:
            json.dump(summary, f, indent=4)

    # ======================================================

    def plot_confusion(self):
        
        cm = confusion_matrix(self.y_test, self.best_prediction, normalize = "true")

        disp = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = self.best_pipeline.classes_)

        disp.plot(xticks_rotation = 45)

        plt.tight_layout()

        plt.savefig(OUTPUT_DIR / "confusion_matrix.png")

        plt.show()

    # ======================================================

    def process(self):

        print("=" * 60)

        print("Damage Mode Training")

        print("=" * 60)

        self.split_dataset()

        self.train_models()

        self.save_model()

        self.plot_confusion()

        print()

        print(self.results)

        print()

        print(f"Best Model : {self.best_name}")

        print(f"Accuracy   : {self.best_metrics['Accuracy']:.4f}")

        return self.best_pipeline


# ======================================================

if __name__ == "__main__":

    trainer = DamageModeTrainer()

    trainer.process()









