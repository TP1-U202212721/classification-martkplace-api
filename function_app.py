import azure.functions as func
import json


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "ok"}),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="classification", methods=["POST"])
def classification(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
        from utils.ml import predict_risk
        result = predict_risk(data)
        if hasattr(result, "item"):
            result = result.item()

        return func.HttpResponse(
            json.dumps({"result": result}),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "El cuerpo de la petición no contiene un JSON válido."}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )