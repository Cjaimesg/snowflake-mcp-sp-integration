

-- Replace the following with your database and schema names if is necessary
USE DATABASE sample_mcp_db;
USE SCHEMA sample_mcp_schema;

-- Create a procedure that returns a table with input text and number
CREATE OR REPLACE PROCEDURE SOME_TABLE(SOME_TEXT VARCHAR, A_NUMBER INT)
RETURNS TABLE (SOME_TEXT VARCHAR, A_NUMBER INT)
LANGUAGE SQL
COMMENT ='This procedure returns a table with the input text and number.
SOME_TEXT: Input text
A_NUMBER: Input number
Output table has columns: SOME_TEXT and A_NUMBER'
AS
DECLARE
  res RESULTSET DEFAULT (SELECT :SOME_TEXT AS SOME_TEXT, :A_NUMBER AS A_NUMBER);
BEGIN
  RETURN TABLE(res);
END;

-- Create a procedure that returns a message with the input text
CREATE OR REPLACE PROCEDURE SAMPLE_MESAGE("MESSAGE" VARCHAR)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
COMMENT='This procedure returns a message with the input text. 
Imput text is: Message text
Output text is: Confirmation message'
EXECUTE AS CALLER
AS '
  return "Received message: " + MESSAGE
';

-- Create the same procedure but with two parameters
CREATE OR REPLACE PROCEDURE SAMPLE_MESAGE("MESSAGE_1" VARCHAR, "MESSAGE_2" VARCHAR)
RETURNS VARCHAR
LANGUAGE JAVASCRIPT
COMMENT='This procedure returns a message with the input text. 
MESSAGE_1: Message text
MESSAGE_2: Additional text
Output text is: Confirmation message'
EXECUTE AS CALLER
AS '
  return "Received message: " + MESSAGE_1 + " and additional text: " + MESSAGE_2
';