import axios from "axios";
import { BASE_URL } from "../constants";

async function continueConversation(
  updatedMessages,
  max_length = 236,
  model = null,
  timeout = 30000
) {
  const response = await axios.post(
    `${BASE_URL}/api/conversation`,
    {
      messages: updatedMessages,
      max_length: max_length,
      model: model,
    },
    {
      timeout: timeout,
    }
  );
  return [response.data];
}
export { continueConversation };
