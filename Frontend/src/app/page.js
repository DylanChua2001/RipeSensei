'use client';
import React, { useState, useEffect } from 'react';
import { Client } from 'paho-mqtt';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register the components needed for Chart.js
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function App() {
  const [messages, setMessages] = useState([]);  // State to hold received messages
  const [timestamps, setTimestamps] = useState([]); // State to hold time for X-axis

  // Function to initialize the MQTT connection and subscribe to the topic
  useEffect(() => {
    // Create a client instance
    const client = new Client("75a6d5883ba24aafa29b3f1f830f6464.s1.eu.hivemq.cloud", 8884, "clientId-" + Math.random());

    // Set callback handlers
    client.onConnectionLost = (responseObject) => {
      if (responseObject.errorCode !== 0) {
        console.log("Connection lost:", responseObject.errorMessage);
      }
    };

    client.onMessageArrived = (message) => {
      const messageString = message.payloadString;
      const messageValue = parseFloat(messageString); // Convert message to a number
      if (!isNaN(messageValue)) {
        setMessages((prevMessages) => [...prevMessages, messageValue]); // Append new message to state
        setTimestamps((prevTimestamps) => [...prevTimestamps, new Date().toLocaleTimeString()]); // Add the timestamp
      }
    };

    // Connect the client
    client.connect({
      onSuccess: () => {
        console.log("Connected to MQTT broker");
        client.subscribe("test/raspberrypi/data");  // Subscribe to your topic
      },
      useSSL: true,
      userName: "hivemq.webclient.1728458341347", // Replace with your username
      password: "O7K!8S%?b2F&tXg6sDdv",  // Replace with your password
    });

    // Cleanup function to disconnect when the component is unmounted
    return () => {
      client.disconnect();
    };
  }, []);

  // Prepare data for the line chart
  const chartData = {
    labels: timestamps,  // X-axis will display the time the message was received
    datasets: [
      {
        label: 'MQTT Data Over Time',
        data: messages,  // Y-axis will display the message values
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
      },
    ],
  };

  // Chart options
  const options = {
    responsive: true,
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Time',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Value',
        },
        beginAtZero: true,  // Start the Y-axis at 0
      },
    },
  };

  return (
    <div>
      <h1>MQTT Data from Paho MQTT Client</h1>
      <Line data={chartData} options={options} />
    </div>
  );
}
