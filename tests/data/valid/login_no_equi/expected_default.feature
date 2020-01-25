Feature: User Log In
  ...

  Background:
    Given There is an existing user with username <username>, email <email> and password <password>
      | username | email              | password      |
      | john doe | x                  | ABCD1234!?    |
      | jane doe | jane.doe@gmail.com | abcdefgh1.aba |
