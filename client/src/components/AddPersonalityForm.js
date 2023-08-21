import { useState } from "react";
import axios from "axios";
import { BASE_URL } from "../constants";

const AddPersonalityForm = () => {
  const [personality, setPersonality] = useState("");
  const [characterName, setCharacterName] = useState("");
  const [description, setDescription] = useState("");
  const [handle, setHandle] = useState("");

  const handlePersonalityChange = (e) => {
    setPersonality(e.target.value);
  };

  const handleNameChange = (e) => {
    setCharacterName(e.target.value);
  };

  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleHandleChange = (e) => {
    setHandle(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    let data = {
      name: characterName,
      description: description,
      llm_personality: personality,
      handle: handle,
    };
    axios.post(BASE_URL + "/api/add-personality", data);
  };

  return (
    <div className="App">
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <p>
            "The character will introduce themselves as follows: 'Hi, I am
            [name]. I am [short description]". For example:"Hi, I am [Anna]. I
            am [a science officer on the first manned mission to Mars]" '
          </p>
          <label htmlFor="characterName">Name</label>
          <input
            type="text"
            name="characterName"
            id="characterName"
            value={characterName}
            onChange={handleNameChange}
          />
          <label htmlFor="description">Short description</label>
          <input
            type="text"
            size="50"
            name="description"
            id="description"
            value={description}
            onChange={handleDescriptionChange}
          />
          <label htmlFor="book">LLM instruction</label>
          <textarea
            type="text"
            name="personality"
            id="personality"
            rows="5"
            cols="40"
            value={personality}
            onChange={handlePersonalityChange}
          />
          <label htmlFor="handle">Handle</label>
          <input
            type="text"
            name="handle"
            id="handle"
            value={handle}
            onChange={handleHandleChange}
          />
          <button type="submit">Add this chat personality</button>
        </form>
      </div>
    </div>
  );
};

export default AddPersonalityForm;
