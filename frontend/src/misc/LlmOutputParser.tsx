import React from "react";

interface BeautifyLLMOutputProps {
  text: string;
}

const BeautifyLLMOutput: React.FC<BeautifyLLMOutputProps> = ({ text }) => {
  const lines = text.split("\n");
  const elements: React.JSX.Element[] = [];
  let currentListItems: string[] = [];

  const processInlineHtml = (line: string): string => {
    let processedLine = line.replace(/<i>(.*?)<\/i>/g, "<em>$1</em>");
    processedLine = processedLine.replace(
      /<b>(.*?)<\/b>/g,
      "<strong>$1</strong>"
    );
    return processedLine;
  };

  const flushList = (keyPrefix: string) => {
    if (currentListItems.length > 0) {
      elements.push(
        <ul
          key={`${keyPrefix}-ul-${elements.length}`}
          className="list-disc list-inside space-y-1 my-2 pl-4"
        >
          {currentListItems.map((item, index) => (
            <li
              key={`${keyPrefix}-li-${index}`}
              dangerouslySetInnerHTML={{ __html: processInlineHtml(item) }}
            />
          ))}
        </ul>
      );
      currentListItems = [];
    }
  };

  lines.forEach((line, index) => {
    const trimmedLine = line.trim();
    if (trimmedLine.startsWith("* ")) {
      const listItemText = trimmedLine.substring(2).trim();
      if (listItemText) {
        currentListItems.push(listItemText);
      }
    } else {
      flushList(`line-${index}-pre`);

      if (trimmedLine) {
        elements.push(
          <p
            key={`p-${index}`}
            className="my-1"
            dangerouslySetInnerHTML={{ __html: processInlineHtml(trimmedLine) }}
          />
        );
      }
    }
  });

  flushList("final");

  return <>{elements}</>;
};

export default BeautifyLLMOutput;
