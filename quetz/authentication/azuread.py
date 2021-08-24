from .oauth2 import OAuthAuthenticator

class AzureADAuthenticator(OAuthAuthenticator):
    """Use Microsoft Azure Active Directory account to authenticate users with Quetz. 
    """

    provider = "azuread"
    server_metadata_url = "https://login.microsoftonline.com/organizations/v2.0/.well-known/openid-configuration"
    
    # oauth client params
    access_token_url = "https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
    authorize_url = "https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize"
    api_base_url = "https://login.microsoftonline.com/organizations/v2.0"
    scope =  "openid profile email"

    # endpoint urls
    validate_token_url = "https://graph.microsoft.com/oidc/userinfo"
    revoke_url = "https://login.microsoftonline.com/organizations/oauth2/v2.0/logout"

    async def userinfo(self, request, token):
        profile = await self.client.parse_id_token(request, token)
        custom_profile = {
            "id": profile["sub"],
            "name": profile["name"],
            "avatar_url": profile['picture'],
            "login": profile["email"],
        }
        return custom_profile
    
    def configure(self, config):
        if config.configured_section("azuread"):
            self.client_id = config.azuread_client_id
            self.client_secret = config.azuread_client_secret
            self.is_enabled = True
        else:
            self.is_enabled = False
        
        super().configure(config)