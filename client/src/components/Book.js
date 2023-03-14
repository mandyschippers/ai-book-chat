import React, { useEffect, useState } from "react";
import { BASE_URL } from "../constants";
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageGroup,
  MessageInput,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react";
import axios from "axios";

const Book = (props) => {
  const [book, setBook] = useState("");
  const [character, setCharacter] = useState("");
  const [messages, setMessages] = useState([]);
  const [typing, setTyping] = useState(false);

  const fetchBookByHandle = async (handle) => {
    const response = await axios.get(`${BASE_URL}/api/books/${handle}`);
    setBook(response.data.book.book);
    setCharacter(response.data.character);
    setMessages(
      response.data.messages.filter((message) => message.role !== "system")
    );
    console.log(response.data);
  };

  const continueConversation = async (
    innerHtml,
    textContent,
    innerText,
    nodes
  ) => {
    const question = innerText;
    let updatedMessages = [...messages, { content: question, role: "user" }];
    setMessages(updatedMessages);
    setTyping(true);
    const response = await axios.post(`${BASE_URL}/api/conversation`, {
      messages: updatedMessages,
      question: question,
    });
    setTyping(false);
    setMessages(response.data);
  };

  useEffect(() => {
    fetchBookByHandle(props.handle);
  }, []);

  return (
    <div>
      <h1>
        Talk to {character} from {book}
      </h1>
      <div style={{ position: "relative", height: "500px" }}>
        <MainContainer>
          <ChatContainer>
            <MessageList>
              {messages &&
                messages.map((message, idx) => {
                  return (
                    <MessageGroup
                      key={idx}
                      direction={
                        message.role == "assistant" ? "incoming" : "outgoing"
                      }
                      sender={message.role == "assistant" ? character : "You"}
                    >
                      <MessageGroup.Messages>
                        <Message
                          model={{
                            message: message.content,
                            sentTime: "just now",
                            sender:
                              message.role == "assistant" ? character : "You",
                          }}
                        />
                      </MessageGroup.Messages>
                    </MessageGroup>
                  );
                })}
              {typing && <TypingIndicator content={`${character} is typing`} />}
            </MessageList>
            <MessageInput
              placeholder="Type message here"
              onSend={continueConversation}
            />
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  );
};

export default Book;
