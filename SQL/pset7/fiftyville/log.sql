-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Check all crimes for the day, the criminal could be running away with a stolen vehichle
SELECT description FROM crime_scene_reports WHERE year = 2020 AND month = 07 AND day = 28;

-- Check the courthouse logs within 1h of the crime time stamp
SELECT activity, license_plate, hour, minute FROM courthouse_security_logs WHERE year = 2020 AND month = 07 AND day = 28 AND hour BETWEEN 9 AND 11;

-- Check the interviews from the day
SELECT name, transcript FROM interviews WHERE year = 2020 AND month = 07 AND day = 28;

-- The three witnesses are Ruth, Eugene and Raymond
-- The thief left between 10:15 and 10:25
-- The thief was at the ATM on Fifer Street before Eugene got to the courthouse
-- The theif talked with someone on the phone for < 1 min
-- The thief was on the earliest flight the next day
-- the accomplice purchased the ticket

-- Create Suspects list from people left the courhouse after the crime
SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 07 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25);

-- Check the ATM recods
SELECT * FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND year = 2020 AND month = 07 AND day = 28;

-- Check for people who were at the ATM and left the courthouse within 10min of the crime
SELECT DISTINCT(Name) FROM people
JOIN bank_accounts, atm_transactions, courthouse_security_logs
ON people.id = bank_accounts.person_id AND bank_accounts.account_number = atm_transactions.account_number AND people.license_plate = courthouse_security_logs.license_plate
WHERE atm_location LIKE "%Fifer Street%" AND atm_transactions.year = 2020 AND atm_transactions.month = 07 AND atm_transactions.day = 28 AND
people.license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE courthouse_security_logs.year = 2020 AND courthouse_security_logs.month = 07 AND courthouse_security_logs.day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25);
-- Ernest, Russell, Elizabeth and Danielle were, both, at the ATM and the courthouse that day

-- Phone calls within 10min of the crime time with duration < 1 min
SELECT caller, receiver, duration FROM phone_calls WHERE year = 2020 AND month = 07 AND day = 28 AND duration < 60;

-- Phone calls made from any of the suspects on the day of the crime and < 1 min duration:
SELECT name, receiver FROM people
JOIN phone_calls
ON people.phone_number = caller
WHERE year = 2020 AND month = 07 AND day = 28 AND duration < 60
AND caller IN (SELECT phone_number FROM people WHERE name IN ('Ernest', 'Russell', 'Elizabeth', 'Danielle'));

-- Only Ernest made a call for < 1 min that day, was at the ATM and the courthouse - HE'S THE BAD GUY!

-- Where to was the earliest flight on 29th and was Ernest on the passengers list?
SELECT destination_airport_id, hour, minute FROM flights WHERE year = 2020 AND month = 07 AND day = 29 ORDER BY hour DESC, minute DESC;
-- Earliest flight was at 8:20

-- Where was the flight going - LONDON
SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2020 AND month = 07 AND day = 29 AND hour = 8 AND minute = 20);

-- Was Ernest on the flight? - YES
SELECT passengers.passport_number, seat FROM passengers
JOIN people, flights
ON people.passport_number = passengers.passport_number AND flights.id = passengers.flight_id
WHERE name = "Ernest" AND year = 2020 AND month = 07 AND day = 29 AND hour = 8 AND minute = 20;

-- Who Ernest talked to on the phone? - Berthold!
SELECT name FROM people
WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year = 2020 AND month = 07 AND day = 28 AND duration < 60
AND caller = (SELECT phone_number FROM people WHERE name = "Ernest"));