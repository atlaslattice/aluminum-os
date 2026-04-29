#!/usr/bin/env python3
"""
Grokbrain v4.0 - Grok JSON Chat Export Parser
Handles nested conversation format from xAI Grok exports
"""

import json
import os
from typing import List, Dict
from datetime import datetime
import structlog

logger = structlog.get_logger()

def parse_grok_export(file_path: str) -> List[Dict]:
    """
    Parse Grok chat export JSON into input/output artifact pairs

    Expected format:
    {
      "conversations": [{
        "conversation": {"id": "...", "title": "..."},
        "responses": [
          {"response": {"message": "...", "sender": "human", ...}},
          {"response": {"message": "...", "sender": "assistant", "thinking_trace": "...", ...}}
        ]
      }]
    }

    Returns: List of {input, output, timestamp, source_file, metadata} dicts
    """
    artifacts = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle both single conversation and array of conversations
        conversations = data.get('conversations', [])
        if not conversations:
            logger.warning("no_conversations_found", file=file_path)
            return artifacts

        for conv_wrapper in conversations:
            conversation = conv_wrapper.get('conversation', {})
            responses = conv_wrapper.get('responses', [])

            conv_id = conversation.get('id', 'unknown')
            conv_title = conversation.get('title', 'Untitled')

            # Extract Q&A pairs (human -> assistant)
            i = 0
            while i < len(responses):
                current = responses[i].get('response', {})

                # Look for human message
                if current.get('sender') == 'human':
                    human_msg = current.get('message', '')
                    human_time = current.get('create_time', {})

                    # Look for assistant response
                    assistant_msg = ''
                    assistant_thinking = ''
                    assistant_time = None

                    if i + 1 < len(responses):
                        next_resp = responses[i + 1].get('response', {})
                        if next_resp.get('sender') == 'assistant':
                            assistant_msg = next_resp.get('message', '')
                            assistant_thinking = next_resp.get('thinking_trace', '')
                            assistant_time = next_resp.get('create_time', {})
                            i += 1  # Skip next since we processed it

                    # Create artifact
                    if human_msg and assistant_msg:
                        # Parse timestamp
                        timestamp = None
                        if isinstance(human_time, dict) and '$date' in human_time:
                            timestamp_ms = human_time['$date'].get('$numberLong')
                            if timestamp_ms:
                                timestamp = datetime.fromtimestamp(int(timestamp_ms) / 1000).isoformat()

                        if not timestamp:
                            timestamp = datetime.now().isoformat()

                        artifact = {
                            'input': human_msg,
                            'output': assistant_msg,
                            'timestamp': timestamp,
                            'source_file': os.path.basename(file_path),
                            'metadata': {
                                'conversation_id': conv_id,
                                'conversation_title': conv_title,
                                'thinking_trace': assistant_thinking,
                                'model': current.get('model', 'unknown')
                            }
                        }

                        artifacts.append(artifact)
                        logger.debug("artifact_created",
                                   conv_id=conv_id,
                                   input_len=len(human_msg),
                                   output_len=len(assistant_msg))

                i += 1

        logger.info("grok_export_parsed",
                   file=file_path,
                   artifacts_count=len(artifacts),
                   conversations=len(conversations))

        return artifacts

    except json.JSONDecodeError as e:
        logger.error("json_decode_error", file=file_path, error=str(e))
        return []
    except Exception as e:
        logger.error("parse_error", file=file_path, error=str(e))
        return []


def detect_export_format(file_path: str) -> str:
    """
    Detect chat export format (grok, openai, gemini, deepseek, simple)
    Returns: Format name as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Grok format: has "conversations" array
        if 'conversations' in data:
            return 'grok'

        # Simple format: has "messages" or "title" + "messages"
        if 'messages' in data:
            messages = data['messages']
            if messages and isinstance(messages, list):
                first_msg = messages[0]
                # Check for role-based format (OpenAI/Gemini)
                if 'role' in first_msg:
                    return 'simple'
                # Check for sender-based format (potential variant)
                if 'sender' in first_msg:
                    return 'simple'

        return 'unknown'

    except Exception as e:
        logger.error("format_detection_error", file=file_path, error=str(e))
        return 'unknown'
