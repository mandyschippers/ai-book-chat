import React, { useEffect, useState } from "react";
import bookStyles from "./Book.module.css";
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

const Personality = (props) => {
  const [books, setBooks] = useState("");
  const [name, setName] = useState("");
  const [messages, setMessages] = useState([]);
  const [typing, setTyping] = useState(false);
  const [handle, setHandle] = useState(props.handle);

  const fetchPersonalityByHandle = async (handle) => {
    const response = await axios.get(`${BASE_URL}/api/personalities/${handle}`);
    setName(response.data.name);
    setBooks(response.data.books);
    setMessages(response.data.messages);
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
      max_length: 236,
      model: null,
    });
    setTyping(false);
    setMessages(response.data);
  };

  useEffect(() => {
    fetchPersonalityByHandle(props.handle);
  }, []);

  useEffect(() => {
    fetchPersonalityByHandle(handle);
  }, [handle]);

  return (
    <div className={bookStyles.container}>
      <h1 className={bookStyles.title}>Talk to {name}</h1>
      <div className={bookStyles.chatWrapper}>
        <MainContainer>
          <ChatContainer>
            <MessageList
              typingIndicator={
                typing && <TypingIndicator content={`${name} is typing`} />
              }
            >
              {messages &&
                messages
                  .filter((message) => message.role !== "system")
                  .map((message, idx) => {
                    return (
                      <MessageGroup
                        key={idx}
                        direction={
                          message.role == "assistant" ? "incoming" : "outgoing"
                        }
                        sender={message.role == "assistant" ? name : "You"}
                      >
                        <MessageGroup.Messages>
                          <Message
                            model={{
                              message: message.content,
                              sentTime: "just now",
                              sender:
                                message.role == "assistant" ? name : "You",
                            }}
                          />
                        </MessageGroup.Messages>
                      </MessageGroup>
                    );
                  })}
            </MessageList>
            <MessageInput
              placeholder={"Type your question for " + name + " here"}
              onSend={continueConversation}
            />
          </ChatContainer>
        </MainContainer>
      </div>
      {/* <a href="https://www.edumetaverse.com.au/" target="_blank">
        <img
          src="https://i.ibb.co/0QKJQhz/IMG-F58-DB70-A6715-1.jpg"
          alt="EDUmetaverse"
          className={bookStyles.logo}
        />
      </a> */}
    </div>
  );
};

export default Personality;
