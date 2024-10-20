from unittest.mock import patch
from app.routers.ai_response import generate_ai_response


def test_generate_ai_response():
    comment_content = "This is a test comment."

    # Mock the Google AI API
    with patch("app.routers.ai_response.model.start_chat") as mock_start_chat:
        mock_chat_session = mock_start_chat.return_value
        mock_chat_session.send_message.return_value.text = "This is a mock AI response."

        ai_response = generate_ai_response(comment_content)

        assert ai_response == "This is a mock AI response."
        mock_chat_session.send_message.assert_called_once_with(
            f"Respond to the comment: {comment_content}"
        )
