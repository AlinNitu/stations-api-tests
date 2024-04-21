@regression
Feature: Testing that a station is compliant

  """
  The following approach contains modular steps that allows for customization and provides us the ability to create
  multiple testing scenarios with the already existing steps, and tests commands separately if needed.

  This approach will produce the desired result, i.e. validate which stations are compliant and which are not.
  But it won't pinpoint exactly what are all the issues with each station tested, due to the synchronous approach,
  because some commands won't be executed if the previous one failed.

  For that we would need a mechanism that allows us to send all requests, collect the responses, and validate all
  of them at once.
  At the bottom of the page I've implemented this approach as well.
  """


  # At the moment of writing these tests, all are failing, as in none of them meet all valid criteria at once.
  # Not sure if this was intended. So I will add some individual command tests, just to have some valid results.
  @all-commands-sync
  Scenario Outline: A station with a particular station ID meets all criteria to be compliant
    When a test request with command "getVersion" is sent to station ID <station_id>
    Then response status code is 200
    And the tested station has compliant version
    When a test request with command "getInterval" is sent to station ID <station_id>
    Then response status code is 200
    And the tested station has compliant interval
    When a test request with command "setValues" and payload number <payload_number> is sent to station ID <station_id>
    Then response status code is 200
    And the tested station is compliant for setting values
    Examples:
      | station_id | payload_number |
      | 1          | 2              |
      | 2          | 9              |
      | 3          | 2              |
      | 4          | 2              |
      | 5          | 2              |

  @get-version
  Scenario Outline: A station with a particular station ID has compliant version
    When a test request with command "getVersion" is sent to station ID <station_id>
    Then response status code is 200
    And the tested station has compliant version
    Examples:
      | station_id |
      | 1          |
      | 2          |
      | 3          |
      | 4          |
      | 5          |

  @get-interval
  Scenario Outline: A station with a particular station ID has compliant interval
    When a test request with command "getInterval" is sent to station ID <station_id>
    Then response status code is 200
    And the tested station has compliant interval
    Examples:
      | station_id |
      | 1          |
      | 2          |
      | 3          |
      | 4          |
      | 5          |

  @all-commands-async
  Scenario: Verify that all criteria is met for a station to be compliant
    When all test requests are sent to station ID 4
    Then the tested stations are compliant for all commands
