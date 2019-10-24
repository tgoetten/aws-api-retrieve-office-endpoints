#!/usr/bin/env python3

from aws_cdk import core

from aws_api_retrieve_office_endpoints.aws_api_retrieve_office_endpoints_stack import AwsApiRetrieveOfficeEndpointsStack


app = core.App()
AwsApiRetrieveOfficeEndpointsStack(app, "aws-api-retrieve-office-endpoints")

app.synth()
