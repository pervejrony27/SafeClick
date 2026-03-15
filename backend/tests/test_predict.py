from backend.ml.predict import predict_url


class DummyModel:
    def predict(self, X):
        return ["legitimate"]


def test_predict_url():
    pred = predict_url(DummyModel(), {"length": 10.0})
    assert pred == "legitimate"
