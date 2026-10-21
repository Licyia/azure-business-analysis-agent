"""Send a prompt to a Microsoft Foundry Business Analysis agent."""

import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


def main() -> None:
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    agent_name = os.environ.get("FOUNDRY_AGENT_NAME")
    if not endpoint or not agent_name:
        raise SystemExit(
            "Set FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_AGENT_NAME before running."
        )

    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        prompt = input("Ask a Business Analysis question: ").strip()
    if not prompt:
        raise SystemExit("A prompt is required.")

    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(
            endpoint=endpoint,
            credential=credential,
            allow_preview=True,
        ) as project_client,
    ):
        # The agent's instructions and knowledge tool are configured in Foundry.
        openai_client = project_client.get_openai_client(agent_name=agent_name)
        conversation = openai_client.conversations.create()
        response = openai_client.responses.create(
            conversation=conversation.id,
            input=[{"role": "user", "content": prompt}],
        )
        print(response.output_text)


if __name__ == "__main__":
    main()
