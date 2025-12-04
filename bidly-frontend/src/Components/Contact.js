import React from "react";
import { SocialIcon } from 'react-social-icons'
import { ReactDOM } from "react";

const Contact = () => {
  return (
    <div className="contact-page-wrapper">
      <h1 className="primary-heading">Contact Me!</h1>
      <h1 className="primary-heading">Let Me Help You Out</h1>
      <div className="contact-form-container">
        <input type="text" placeholder="yourmail@gmail.com" />
        <button className="secondary-button">Submit</button>
      </div>

      <div className="socialIcons">
        <SocialIcon network="twitter" url="https://twitter.com/original_ethio"/>
        <SocialIcon network="linkedin" url="https://www.linkedin.com/in/yosias-hailu-219b80127/"/>
        <SocialIcon network="facebook" />
      </div>
    </div>
  );
};

export default Contact;
