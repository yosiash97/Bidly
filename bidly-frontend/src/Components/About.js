import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

const aboutStyle = {
    color: "white",
    backgroundColor: "#556B2F",
    padding: "10px",
    fontFamily: "Arial"
  };



const About = () => {
    return (
        <div className="contact-page-wrapper">
        <h1 className="primary-heading">FAQ's</h1>
        
        <h1 className="primary-subheading-question">What is an RFP?</h1>
        <h1 className="primary-subheading-answer">It's a Request for Proposal, AKA a business document that describes and announces a project.</h1>
        <h1 className="primary-subheading-question">Is this just for Civil Engineering RFP's?</h1>
        <h1 className="primary-subheading-answer">Nope, you can get any Government project posted on their website! Event, School, Construction RFP's, etc. </h1>
        <h1 className="primary-subheading-question">Can I only source RFP's within 100 miles?</h1>
        <h1 className="primary-subheading-answer">Nope, it can be as far as your heart desires, just contact me!</h1>

        <div className="contact-form-container">
            <h1 className="primary-subheading">Questions?</h1>
          <input type="text" placeholder="yourmail@gmail.com" />
          <button className="secondary-button">Submit</button>
        </div>
      </div>
    );
};

export default About;
