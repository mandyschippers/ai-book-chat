import axios from "axios";
import { BASE_URL } from "../constants";

async function continueConversation(updatedMessages, question) {
  const response = await axios.post(`${BASE_URL}/api/conversation`, {
    messages: updatedMessages,
    question: question,
  });
  return [response.data];
}
export { continueConversation };
