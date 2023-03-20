import React, { useEffect, useState } from "react";
import bookStyles from "./Book.module.css";
import { BASE_URL } from "../constants";
import { continueConversation } from "../services/ConversationService";
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

const SecretOracle = (props) => {
  const [messages, setMessages] = useState([]);
  const [character, setCharacter] = useState("the Secret Oracle");
  const [typing, setTyping] = useState(false);

  const getInitialMessage = async () => {
    const response = await axios.get(`${BASE_URL}/api/secret-oracle`);
    setCharacter(response.data.character);
    setMessages(
      response.data.messages.filter((message) => message.role !== "system")
    );
  };

  useEffect(() => {
    getInitialMessage();
  }, []);

  const handleConversation = (innerText) => {
    const question = innerText;
    let updatedMessages = [...messages, { content: question, role: "user" }];
    setMessages(updatedMessages);
    setTyping(true);
    continueConversation(updatedMessages, question, 2048, "gpt-4", 60000).then(
      (response) => {
        setTyping(false);
        setMessages(response[0]);
      }
    );
  };

  return (
    <div className={bookStyles.container}>
      <h1 className={bookStyles.title}>Talk to {character}</h1>
      <div className={bookStyles.chatWrapper}>
        <MainContainer>
          <ChatContainer>
            <MessageList
              typingIndicator={
                typing && <TypingIndicator content={`${character} is typing`} />
              }
            >
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
            </MessageList>
            <MessageInput
              placeholder={"Type your question for " + character + " here"}
              onSend={handleConversation}
            />
          </ChatContainer>
        </MainContainer>
      </div>
      <a href="https://www.edumetaverse.com.au/" target="_blank">
        <img
          src="https://i.ibb.co/0QKJQhz/IMG-F58-DB70-A6715-1.jpg"
          alt="EDUmetaverse"
          className={bookStyles.logo}
        />
      </a>
    </div>
  );
};

export default SecretOracle;
