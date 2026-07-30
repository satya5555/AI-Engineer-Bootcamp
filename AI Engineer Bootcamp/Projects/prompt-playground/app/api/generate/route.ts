import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({
  apiKey: process.env.GEMINI_API_KEY,
});

export async function POST(request: Request) {
  try {
    const { prompt, temperature = 0.7 } = await request.json();

    if (!prompt) {
      return Response.json({ error: "Prompt is required" }, { status: 400 });
    }

    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: prompt,
      config: {
        temperature,
      },
    });

    return Response.json({
      result: response.text,
    });
  } catch (error) {
    console.error("Gemini API error:", error);

    return Response.json(
      { error: "Failed to generate response" },
      { status: 500 },
    );
  }
}
