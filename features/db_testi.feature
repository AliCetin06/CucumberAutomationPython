
# Feature: This file validates database operations for customer management using utility classes
Feature: Customer Database Validation

  # Scenario: Verifying that a specific customer exists in our existing tables
  Scenario: Verify an existing customer is successfully retrieved from the database
    Given The database connection is established
    Then The system should verify that a customer named "Atelier graphique" exists in the database