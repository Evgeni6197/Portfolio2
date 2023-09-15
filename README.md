# Auction

 ### 1.  [Video Demonstration ](https://youtu.be/5kOIZerd7EA)

 ### 2. Launching

   The procedure described below presumes that you are using Bash. 
   Inside an empty folder, run: 
   
   ```
   git clone https://github.com/Evgeni6197/Portfolio2.git
   cd Portfolio2
   python3 -m venv ./venv
   source venv/bin/activate
   python -m pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
### 3. Content
   - User registration
   - Posting listings and uploading pictures
   - Making bids on listings
   - Adding comments
   - Placing listings in the watchlist
   - Querying listings by category
   - *My Listings*  page 
       - Closing auctions
       - Deleting listings
       - Inspecting bids
