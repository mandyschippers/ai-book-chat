import axios from "axios";

//a service for conversations
const ConversationService = {
  //get all conversations
  getConversations: async () => {
    const response = await axios.get(`${BASE_URL}/api/conversations`);
    return response.data;
  },
};

export default ConversationService;
