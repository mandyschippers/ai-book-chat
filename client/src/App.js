import axios from "axios";
import { format } from "date-fns";
import { useEffect, useState } from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import Book from "./components/Book";
import Personality from "./components/Personality";
import { BASE_URL } from "./constants";
import Hogwarts from "./components/Hogwarts";
import SecretOracle from "./components/SecretOracle";

//create axios headers to allow Access-Control-Allow-Origin
axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";

function App() {
  const [book, setBook] = useState("");
  const [characters, setCharacters] = useState("");
  const [handle, setHandle] = useState("");

  const handleBookChange = (e) => {
    setBook(e.target.value);
  };

  const handleCharacterChange = (e) => {
    setCharacters(e.target.value);
  };

  const handleHandleChange = (e) => {
    setHandle(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    let data = {
      book: book,
      characters: characters,
      handle: handle,
    };
    axios.post(BASE_URL + "/api/books", data);
  };

  return (
    <Router>
      {/* <header className="App-header">
        <nav>
          <ul>
            <li>
              <Link to={"/books/charlottes-web"}>Charlotte's Web</Link>
            </li>
            <li>
              <Link to="/books/james-and-the-giant-peach">
                James and the Giant Peach
              </Link>
            </li>
            <li>
              <Link to="/books/a-wrinkle-in-time">A Wrinkle in Time</Link>
            </li>
          </ul>
        </nav>
      </header> */}
      <Switch>
        <Route exact path="/">
          <div className="App">
            <header className="App-header">
              {" "}
              <img
                src="https://i.ibb.co/0QKJQhz/IMG-F58-DB70-A6715-1.jpg"
                alt="EDUmetaverse"
                className="logo"
              />
              AI Book Chat
            </header>
          </div>
        </Route>
        <Route path="/add">
          <div className="App">
            <div className="form-container">
              <form onSubmit={handleSubmit}>
                <label htmlFor="book">Book</label>
                <input
                  type="text"
                  name="book"
                  id="book"
                  value={book}
                  onChange={handleBookChange}
                />
                <label htmlFor="characters">Characters</label>
                <input
                  type="text"
                  name="characters"
                  id="characters"
                  value={characters}
                  onChange={handleCharacterChange}
                />
                <label htmlFor="handle">Handle</label>
                <input
                  type="text"
                  name="handle"
                  id="handle"
                  value={handle}
                  onChange={handleHandleChange}
                />
                <button type="submit">Submit</button>
              </form>
            </div>
          </div>
        </Route>
        <Route
          path={"/books/:handle"}
          render={({ match }) => <Book handle={match.params.handle} />}
        />
        <Route
          path={"/personalities/:handle"}
          render={({ match }) => <Personality handle={match.params.handle} />}
        />
        <Route path={"/hogwarts-library"}>
          <Hogwarts />
        </Route>
        <Route path={"/nothing-to-see-here"}>
          <SecretOracle />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
