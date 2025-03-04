// send request to backend
// get response 
// console logs for debugging


export const getAIMessage = async (userQuery) => {
  try {
    // log to check when request being sent
    console.log("Sending request to backend...");

    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: userQuery }),
    });

    if (!response.ok) {

      throw new Error(`HTTP Error: ${response.status}`);

    }

    // async generator for reading stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    async function* streamResponse() {
      let finalResponse = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        finalResponse += chunk;
        yield chunk; // Real time chunk yielding


        // check received chunks
        console.log("Received Streaming Chunk:", chunk);
      }

      // check final response
      console.log("Final AI Response:", finalResponse);
    }

    return streamResponse(); 

  } catch (error) {
    console.error("API Error:", error);
    return async function* () {
      yield "Error: Could not display the response correctly.";
    };
  }
};
