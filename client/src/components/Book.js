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

const Book = (props) => {
  const [book, setBook] = useState("");
  const [character, setCharacter] = useState("");
  const [messages, setMessages] = useState([]);
  const [typing, setTyping] = useState(false);
  const [handle, setHandle] = useState(props.handle);
  const [updateHandle, setUpdateHandle] = useState(false);

  const fetchBookByHandle = async (handle) => {
    const response = await axios.get(`${BASE_URL}/api/books/${handle}`);
    setBook(response.data.book.book);
    setCharacter(response.data.character);
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
    fetchBookByHandle(props.handle);
  }, []);

  useEffect(() => {
    fetchBookByHandle(handle);
    setUpdateHandle(false);
  }, [handle]);

  return (
    <div className={bookStyles.container}>
      <h1 className={bookStyles.title}>
        Talk to {character} from {book}
      </h1>
      <div className={bookStyles.chatWrapper}>
        <MainContainer>
          <ChatContainer>
            <MessageList
              typingIndicator={
                typing && <TypingIndicator content={`${character} is typing`} />
              }
            >
              {messages &&
                messages.length > 0 &&
                messages
                  .filter((message) => message.role !== "system")
                  .map((message, idx) => {
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
              onSend={continueConversation}
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

export default Book;
