import axios from "axios";
import { format } from "date-fns";
import { useEffect, useState } from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import Book from "./components/Book";
import { BASE_URL } from "./constants";

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
    console.log(data);
    axios.post(BASE_URL + "/api/books", data);
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    const response = await axios.get(`${BASE_URL}/api/books`);
    console.log("data", response.data);
  };

  return (
    <Router>
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
      <Switch>
        <Route exact path="/">
          <div className="App">
            <header className="App-header">AI Book Chat</header>
          </div>
        </Route>
        <Route path="/add">
          <div className="App">
            <header className="App-header">
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
            </header>
          </div>
        </Route>
        <Route
          path={"/books/:handle"}
          render={({ match }) => <Book handle={match.params.handle} />}
        />
      </Switch>
    </Router>
  );
}

export default App;
