from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret: str = "dev-secret"
    gateway_url: str = "http://gateway:8080"
    auth_service_url: str = "http://auth:8001"
    quiz_service_url: str = "http://quiz:8002"
    performance_service_url: str = "http://performance:8003"
    recommendation_service_url: str = "http://recommendation:8004"
    knowledge_graph_service_url: str = "http://knowledge-graph:8005"
    tutor_service_url: str = "http://tutor:8006"
    analytics_service_url: str = "http://analytics:8007"
    redis_url: str = "redis://redis:6379/0"
    postgres_url: str = "postgresql://postgres:postgres@postgres:5432/edgap"
    neo4j_uri: str = "bolt://neo4j:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    llm_provider_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
