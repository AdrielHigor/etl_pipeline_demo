React Native Performance Solutions: Debug Like a Pro
Debugging: the art of being a detective in a crime scene where you're also the prime suspect. While traditional debugging tools help you find out why your perfectly written code (you’d think!) decided to throw a tantrum, certain tools are specifically designed to provide insights into performance bottlenecks, enabling developers to improve the efficiency of their applications.

Performance in React Native isn’t exactly a cakewalk. It’s a delicate balancing act between JavaScript, native modules, and the occasional head-scratcher. To achieve smooth performance, you first need to know where the bottlenecks are—and that’s where debugging tools come in. Let’s dive in!

Traditional Debugging Tools
React Native offers several built-in tools to assist in the debugging process:

In-App Developer Menu: Shake your phone like a Polaroid picture (or use keyboard shortcuts) to open the developer menu. You’ll find options like hot reloading, element inspection, and a dash of performance profiling.

Chrome DevTools: Connect to your app and debug JavaScript execution, monitor network requests, and keep an eye on every moving part.

These are fine tools, but they often leave you wondering about what’s slowing things down. Let’s level up.

Performance-Focused Debugging Tools
When it comes to optimizing React Native applications, having the right tools is crucial. These performance-focused debugging tools go beyond basic error tracking—they help you understand the inner workings of your app, identify performance bottlenecks, and make data-driven optimization decisions. Let's explore some of the most powerful tools in a React Native developer's performance optimization toolkit.

1 - Why Did You Render (WDYR)
WDYR is like a lie detector test for React components—it tells you exactly when and why they re-render. Imagine spotting that one child component re-rendering 500 times because of a single prop change. With WDYR, you can catch and fix these “oops” moments.

Its installation process is very straightforward and simple. Check it out:

Install the package:

npm install @welldone-software/why-did-you-render --save-dev
Create a wdyr.js file in the root directory with the following content:

import React from 'react';
import whyDidYouRender from '@welldone-software/why-did-you-render';

if (process.env.NODE_ENV === 'development') {
  whyDidYouRender(React, {
    trackAllPureComponents: true,
  });
}
Import wdyr.js at the top of your entry file (e.g., index.js):

import './wdyr';
Now, your console will provide detailed logs showing which components are re-rendering and why. You'll see information about prop changes, state updates, and other triggers that cause components to refresh unnecessarily.



2 - React Native DevTools
Meet the shiny new React Native DevTools—a step up from Chrome DevTools. It combines React Inspector, Redux DevTools, and a profiler to track performance issues and visualize bottlenecks.

debugging-rndt-sources-paused-with-device-d1d48a3df5a69d3bf92a16845f0f9c12.jpg
debugging-rndt-sources-paused-with-device-d1d48a3df5a69d3bf92a16845f0f9c12.jpg
Why It’s Awesome:

Profiler: Monitor component renders and check why specific components are slow.
Component Tree: Understand the hierarchy and pinpoint which elements are overworking themselves.
Redux Insights: Track state changes for apps using Redux.
Here's how to quickly enable it:

Upgrade React Native to version 0.70 or later.
Open the DevTools by running npx react-devtools.
With these tools, you can identify exactly which components need optimization and improve your app’s performance.

Why Optimize?
Performance optimization isn't just a technical necessity—it's the difference between an app that delights users and one that frustrates them. Slow load times, laggy interactions, and unresponsive interfaces can turn even the most promising app into a source of user frustration.

When your app runs at a snail’s pace, this is how your users feel:


Don’t let your app be the reason phones meet walls.

Implementing Performance Optimizations
Once performance bottlenecks are identified using the tools above, developers can apply React best practices to optimize their applications:

Memoization: Utilize React.memo to prevent unnecessary re-renders of functional components when their props haven't changed.
useCallback and useMemo Hooks: These hooks help memoize functions and values, ensuring that components do not re-render due to unchanged dependencies.
Pure Components: For class components, extending React.PureComponent enables shallow prop and state comparison, reducing unnecessary updates.
Optimize Lists with FlatList: When rendering large lists, use FlatList instead of ScrollView to improve performance by rendering only visible items.
Avoid Inline Functions: Define functions outside of render methods to prevent re-creation on every render, which can lead to unnecessary re-renders of child components.
Conclusion
Debugging in React Native isn’t just about fixing bugs; it’s about building apps that make users smile instead of rage quit. By using tools like WDYR and the new React Native DevTools, you can identify performance bottlenecks and create buttery-smooth apps.

So, put on your detective hat, squash those bugs, and make your app a joy to use. Your users—and their phones—will thank you.









At Beta Acid, we've been experimenting with integrating Large Language Models (LLMs) into our workflows for over two years now. For our engineering team, GitHub Copilot has been a productivity enhancer, but we've recently started noticing some persistent flaws:

Partial code completions
Seemingly worsening suggestions
Inconsistent use of context from the codebase
Too much copy/pasting into chat windows or other LLMs
A few months ago we began exploring new tools that better integrate into our development workflow. One tool that stood out is Cursor, a fork of VS Code that integrates LLM features throughout the IDE. What sets Cursor apart is its deep integration with context from your codebase, which dramatically improves code suggestions and completion accuracy.

Harnessing the Power of Context
Cursor’s ability to leverage context is its strongest feature. It pulls context directly from your codebase by indexing files and directories, which allows it to understand your project’s structure and dependencies. In addition to this automatic indexing, you can give Cursor additional context by using specific references in chat, such as pointing to files, code snippets, or external documentation.

Here are the main types of context that Cursor uses to improve your workflow:

Codebase Indexing: Cursor indexes your entire codebase, providing it with some understanding of the project’s structure, functions, and classes. This allows the LLM to suggest code that is consistent with your project’s existing patterns and architecture.
@files and @code: Use @files and @code to refer directly to specific files or blocks of code within your project. This ensures that Cursor can pull in relevant snippets or structural elements from your existing codebase.
@docs: Calling @docs allows you to reference external documentation that Cursor can use to better understand your external dependencies. This is especially useful for libraries that change frequently and the LLM might have been trained on outdated material.
@codebase: Use the @codebase symbol to reference your entire codebase contextually in chat. This is useful for tasks that require a broader understanding of your entire project, such as ensuring code consistency across different modules or suggesting improvements based on the overall architecture.
Pro Tips for Using Cursor Effectively
Let’s walk through how Cursor can help us enhance our FastAPI Reference App, which calls the Star Wars API and demonstrates best practices in FastAPI development.

1. Use the Chat Feature for Narrow Tasks
Rather than relying on Cursor’s Composer feature (which generates an entire feature at once), use the Chat feature to tackle smaller, more manageable tasks. You can refine your instructions within the chat and apply them to your file step-by-step. Taking it slow—one small chunk of code at a time—will help you better understand the changes and avoid unwanted behavior.

Letting Cursor build entire features looks great in marketing demos, but is a recipe for trouble in professional development.


2. Choose the Right Model for the Task
For day-to-day code generation and chat interactions, we recommend using Anthropic’s Claude 3.5 Sonnet. It provides the best balance between quality, cost, and speed for routine development. For more in-depth architectural planning, enable usage-based pricing to utilize Open AI’s o1 model. It costs $0.40 per request but provides great results.


3. Add Custom Documentation for Better Context
If the documentation you need isn’t available by default in Cursor you can add it manually and Cursor will scrape and index it for future use. For example, Cursor doesn’t include MJML docs out of the box, but you can have Cursor index the docs to improve code suggestions. Just press CMD+L, type @Docs, select "Add new doc", and provide the URL for the documentation. Cursor will scrape and index the content, allowing you to reference it in chat using @docs.



4. Add a .cursorignore File to Skip Unnecessary Files
You can use a .cursorignore file to tell Cursor to ignore specific files or directories when using the @codebase command in chat. This prevents Cursor from pulling in irrelevant parts of your project, helping it focus on the files that matter most and providing cleaner, more relevant suggestions.

5. Define Team Preferences with .cursorrules
Use a .cursorrules file to standardize how Cursor interacts with your project. This file provides context for each request you make, ensuring consistent code styles and preferences across your team. Sharing these rules helps maintain a cohesive workflow. For inspiration, check out this curated list of .cursorrules files that can be adapted to your team's needs.

6. Provide Clear and Detailed Instructions
When asking Cursor to generate code, provide as much relevant context as possible. For instance, in our reference app we’ve already build a characters endpoint, and now we want to add a new route to manage starships:

Create a new file for the route.
Press CMD+L to open the chat.
Describe your task: "Create a new /starships route that retrieves a list of starships added in the last 24 hours. Use the existing CharacterService and follow the patterns from the /characters endpoint. Implement pagination to limit the results per page, include sorting by creation date, and ensure error handling for when no starships are found. Add validation to check that the created_at field is within the past 24 hours, and update the router to include the new route."

Providing this level of detail will help you get 80% of the way to a working endpoint. Vague prompts like “Create a starships route” won’t follow your existing project structure.

7. Use Notepads for Common Tasks
If you’re frequently asking Cursor to perform similar tasks, the Notepads feature can streamline your workflow. For example, create a Notepad for “AddingNewRoute” in your Star Wars API. This could include common patterns like router structures, service layers, and database calls.

To set up a Notepad, go to Composer > Control Panel > Add Notepad, and store relevant code snippets and file references. When you’re ready, simply reference it in chat using @notepad for consistency across tasks.


8. Don’t Blindly Trust Results
After receiving multiple accurate results from Cursor, it can be tempting to start accepting suggestions without a thorough review. This is a mistake. LLMs can still introduce bugs and hallucinate, particularly when refactoring or suggesting code changes.

Bugs: Even after several successful interactions, review everything carefully. We’ve encountered cases where Cursor changed a file path in a refactor without realizing the template it altered didn’t match.
Non-Optimal Solutions: Cursor may suggest viable but inefficient solutions for your platform. Rely on your expertise to adjust these suggestions to follow best practices.
Conclusion
At Beta Acid, we’re always looking for ways to boost productivity, and while Cursor is a great tool, it’s not magic—it’s simply a smarter interface for working with LLMs. It helps streamline workflows, but ultimately, it's you, the developer, driving the results. Use Cursor’s features to your advantage, but stay grounded—thoughtful engineering always comes first.













Sentiment Analysis is certainly not a new concept, but with powerful modern AI tools it is becoming incredibly easy to do. Here we’ll go through what it is, common use cases for it, and how we can gather actionable data from natural language with just a few lines of code.

For those who are unfamiliar with the concept, Sentiment Analysis (sometimes called “opinion mining”) is the computational process of determining the emotional tone behind a series of words. This is used to gain an understanding of the attitudes, opinions, and emotions expressed within an online mention, be it in social media posts, reviews, forums, or other digital platforms. This emotional tone is typically categorized as positive, negative, or neutral.

GPT-4 is a Large Language Model (LLM) which, by default, returns unstructured natural language as its response. However, OpenAI recently released a new feature called Function Calling which you can use to instruct the LLM to return data in a structured manner (eg. JSON) so that the code you build to call the LLM can, in turn, pass the result off to another function with consistent results.

Using the tools we’ll discuss here, you can build automated sentiment analysis into your product or company process. Automated sentiment analysis, especially in bulk, can be a huge help for companies to prioritize product feedback and identify what customers to respond to.

Common Use Cases for Sentiment Analysis
There are a lot of use cases for performing Sentiment Analysis, but in general it is used to either get a sense of the average sentiment or trending sentiment about a topic, or to quickly identify negative sentiment that needs to be addressed across a broad dataset.

Here are some more practical examples of how sentiment analysis is used by companies today.

Brand Monitoring:
Companies use sentiment analysis to monitor social media and other online platforms to understand public opinion about their brand, products, or services. This helps in managing brand reputation and responding quickly to negative sentiment trends.

Customer Feedback Analysis:
Businesses analyze customer reviews and feedback on their products or services to glean insights about customer satisfaction and identify areas for improvement.

Market Research:
Sentiment analysis is used in market research to understand consumer attitudes towards products, services, or concepts. This can inform product development, marketing strategies, and competitive positioning.

Political Campaigns and Public Opinion:
Politicians and public organizations use sentiment analysis to gauge public opinion on policies, campaigns, and social issues. This can influence policy-making and campaign strategies.

Financial Markets:
In the financial sector, sentiment analysis of news articles, reports, and social media can predict market trends and potential stock movements. Trading performed on this information is at your own risk!

Build a Sentiment Analysis Profiler
Most of our previous articles about AI and Machine Learning tools have highlighted building in Python, which is probably the most common language used for these types of tasks, but many of the products we build use a Javascript stack, so we’ll do this one in Typescript this time.

We’ll be using OpenAI’s Function Calling, accessible via the tools parameter. As of today, Function Calling is only accessible to specific GPT models, so we’ll be using gpt-4-1106-preview. To use the GPT-4 model you’ll need an OpenAI account and API Key.

The code is actually fairly simple and looks as follows:

const determineSentiment = async (prompt: string): Promise<'positive' | 'negative' | 'neutral'> => {
 const chatResponse = await openai.chat.completions.create({
   model: "gpt-4-1106-preview",
   messages: [
     {
       role: "user",
       content: `Determine the sentiment of the following text: "${prompt}". Is it positive, negative, or neutral?`,
     },
   ],
   tools: [
     {
       type: "function",
       function: {
         name: "extractSentiment",
         description: "Extract the sentiment from the user prompt.",
         parameters: {
           type: "object",
           properties: {
             sentiment: {
               type: "string",
               enum: ["positive", "negative", "neutral"],
               description: "The sentiment of the text.",
             },
           },
         },
       },
     },
   ],
 });

 const toolCalls = chatResponse.choices[0].message?.tool_calls;
 if (toolCalls && toolCalls?.length > 0) {
   return JSON.parse(toolCalls[0].function?.arguments).sentiment;
 }
 throw new Error("Failed to determine sentiment");
};
You can execute this function with a simple call like this:

const review = “This was the most delicious fried chicken sandwich I’ve ever had!”;
const sentiment: 'positive' | 'negative' | 'neutral' = await determineSentiment(review);

In this case, we should, of course, receive a result of positive back from the AI. Function Calling and Typescript allows us to receive this data back from the LLM in a type-safe and structured way, allowing us to pass this data on to additional processes.

This is an incredibly simple example, but one that can be used to very easily farm actionable information from vast data sets. For example, perhaps negative reviews get a ticket created in another system indicating that a customer service representative should follow up with the customer. Or maybe sentiment is tracked longitudinally to show how public sentiment for a particular product or topic trends over time.

A more complex example might be a review like the following:

Overall, I really love this product and have been using it for years. It's great! However, the new update is terrible and I hate it. I'm not sure if I will continue using it.

There is both positive and negative sentiment present in this statement and with a few adjustments to the LLM prompts we can explicitly tease out sentiment for each category; perhaps in this example we want to know how the latest product update is being received (not well, apparently).

Wrapping Up
Sentiment Analysis can give you incredibly valuable insights into your business or how the public is feeling about a topic. Getting this data in an automated way is now easier than ever using modern AI tools. Are you sitting on a backlog of customer feedback that is thousands of messages long? Let’s build an AI model that can translate it to actionable feedback for your team.

The team at Beta Acid is solving all kinds of interesting problems using Machine Learning. What can we help you build?