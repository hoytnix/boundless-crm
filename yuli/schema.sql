-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS leads;
DROP TABLE IF EXISTS notes;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  address TEXT,
  city TEXT,
  state TEXT,
  zip INTEGER,
  county TEXT,
  living_square_feet INTEGER,
  year_built INTEGER,
  lot_acres INTEGER,
  lot_square_feet INTEGER,
  land_use TEXT,
  subdivision TEXT,
  apn TEXT,
  legal_description TEXT,
  property_use TEXT,
  units_count INTEGER,
  bedrooms INTEGER,
  bathrooms INTEGER,
  stories INTEGER,
  garage_type TEXT,
  garage_square_feet INTEGER,
  air_conditioning_type TEXT,
  heating_type TEXT,
  fireplaces INTEGER,
  owner_1_first_name TEXT,
  owner_1_last_name TEXT,
  owner_2_first_name TEXT,
  owner_2_last_name TEXT,
  owner_mailing_address TEXT,
  owner_mailing_city TEXT,
  owner_mailing_state TEXT,
  owner_mailing_zip INTEGER,
  ownership_length_months INTEGER,
  owner_type TEXT,
  owner_occupied TEXT,
  vacant TEXT,
  listing_status TEXT,
  listing_price INTEGER,
  days_on_market INTEGER,
  last_updated TEXT,
  listing_agent_full_name TEXT,
  listing_agent_first_name TEXT,
  listing_agent_last_name TEXT,
  listing_agent_email TEXT,
  listing_agent_phone TEXT,
  listing_office_phone TEXT,
  mls_agent_name TEXT,
  mls_agent_phone TEXT,
  mls_agent_office TEXT,
  mls_type TEXT,
  last_sale_date TEXT,
  last_sale_amount INTEGER,
  estimated_value INTEGER,
  estimated_equity INTEGER,
  equity_percent INTEGER,
  open_mortgage_balance INTEGER,
  mortgage_interest_rate INTEGER,
  mortgage_document_date TEXT,
  mortgage_loan_type TEXT,
  lender_name TEXT,
  deed_type TEXT,
  position TEXT,
  tax_amount INTEGER,
  assessment_year INTEGER,
  assessed_total_value INTEGER,
  assessed_land_value INTEGER,
  assessed_improvement_value INTEGER,
  market_value INTEGER,
  market_land_value INTEGER,
  market_improvement_value INTEGER,
  status TEXT,
  default_amount TEXT,
  opening_bid TEXT,
  recording_date TEXT,
  auction_date TEXT
);


CREATE TABLE notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  body TEXT,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
