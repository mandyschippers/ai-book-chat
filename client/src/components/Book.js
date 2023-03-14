import React, { useEffect, useState } from "react";
import { BASE_URL } from "../constants";
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";
import axios from "axios";

const Book = (props) => {
  const [book, setBook] = useState("");
  const [characters, setCharacters] = useState("");

  const fetchBookByHandle = async (handle) => {
    const response = await axios.get(`${BASE_URL}/books/${handle}`);
    console.log("data", response.data);
  };

  //TODO: fetch book by handle and initialise conversation with character

  useEffect(() => {
    fetchBookByHandle(props.handle);
  }, []);

  return (
    <div>
      <h1>Book {props.handle}</h1>
      <div style={{ position: "relative", height: "500px" }}>
        <MainContainer>
          <ChatContainer>
            <MessageList>
              <Message
                model={{
                  message: "Hello my friend",
                  sentTime: "just now",
                  sender: "Joe",
                }}
              />
            </MessageList>
            <MessageInput placeholder="Type message here" />
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  );
};

export default Book;
