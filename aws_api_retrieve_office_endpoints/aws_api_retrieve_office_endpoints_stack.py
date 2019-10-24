from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)


class AwsApiRetrieveOfficeEndpointsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        lambda_retrieve_office_enpoints = _lambda.Function(
            self, 'LambdaRetrieveOfficeEnpointsHandler',
            runtime= _lambda.Runtime.PYTHON_3_7,
            code= _lambda.Code.asset('lambda'), # directory of lambda function(s)
            handler='retrieveofficeenpoints.handler',
        )
        
        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=lambda_retrieve_office_enpoints,
        )