from typing import List

from pydantic import BaseModel


class APIEndpointDetail(BaseModel):
    """
    Details about individual API endpoints, including their operation, path, and purpose.
    """

    path: str
    operation: str
    description: str


class APIIntegrationDetailsResponse(BaseModel):
    """
    Defines the response structure for API integration capabilities and documentation links, offering essential information for third-party developers aiming to integrate with the SpeakEase API.
    """

    api_version: str
    documentation_url: str
    auth_required: bool
    rate_limit_info: str
    supported_endpoints: List[APIEndpointDetail]


def api_integration_details() -> APIIntegrationDetailsResponse:
    """
    Returns API integration capabilities and documentation links.

    Returns:
        APIIntegrationDetailsResponse: Defines the response structure for API integration capabilities and documentation links,
                                       offering essential information for third-party developers aiming to integrate with
                                       the SpeakEase API.
    """
    example_endpoints = [
        APIEndpointDetail(
            path="/api/text-to-speech",
            operation="POST",
            description="Converts input text to speech.",
        ),
        APIEndpointDetail(
            path="/api/speech-to-text",
            operation="POST",
            description="Converts speech audio to text.",
        ),
    ]
    return APIIntegrationDetailsResponse(
        api_version="1.0",
        documentation_url="https://speakease.api/docs",
        auth_required=True,
        rate_limit_info="60 requests per minute",
        supported_endpoints=example_endpoints,
    )
