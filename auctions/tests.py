import datetime
from django.test import Client, TestCase
from django.db.models import Max 

from .helpers import (
    message,
    getListing,
    getWinnerId,
    getComments,
    getCategoryList,
    getSearchResults,
)
from .models import User, Listing, Bid, Category, Comment, Watchlist, Winners


# Unit tests for helper functions
class GetListingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )
        self.listing1 = Listing.objects.create(
            id=1,
            user_id=1,
            item="Listing 1",
            description="Description 1",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )
        self.listing2 = Listing.objects.create(
            id=2,
            user_id=1,
            item="Listing 2",
            description="Description 2",
            date=datetime.datetime.now(),
            starting_bid=1,
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

    def test_get_listing(self):
        """Test the get listing function"""
        retrieved_listing = getListing(1)

        # Check if the retrieved listing matches the required listing
        self.assertEqual(retrieved_listing, self.listing1)

        # Test for a non-existing ID, it should raise a DoesNotExist exception
        with self.assertRaises(Listing.DoesNotExist):
            getListing(9999)


class GetWinnerIdTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            id=1,
            username="user1",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.user2 = User.objects.create_user(
            id=2,
            username="user2",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.listing1 = Listing.objects.create(
            id=1,
            user_id=1,
            item="Listing 1",
            description="Description 1",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )
        self.listing2 = Listing.objects.create(
            id=2,
            user_id=2,
            item="Listing 2",
            description="Description 2",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.bid1 = Bid.objects.create(
            item=self.listing1, user=self.user1, amount=10, date=datetime.datetime.now()
        )

        self.bid2 = Bid.objects.create(
            item=self.listing1, user=self.user2, amount=20, date=datetime.datetime.now()
        )

    def test_get_winner_id(self):
        """Test the getWinnerId function"""
        retrieved_winner_id = getWinnerId(self.listing1)
        self.assertEqual(retrieved_winner_id, 2)

    # Test the function in case there is no winner
    def test_no_winner(self):
        retrieved_winner_id = getWinnerId(self.listing2)
        self.assertEqual(retrieved_winner_id, None)


class GetCommentsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            id=1,
            username="user1",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.user2 = User.objects.create_user(
            id=2,
            username="user2",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.listing1 = Listing.objects.create(
            id=1,
            user_id=1,
            item="Listing 1",
            description="Description 1",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.listing2 = Listing.objects.create(
            id=2,
            user_id=2,
            item="Listing 2",
            description="Description 2",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.comment1 = Comment.objects.create(
            item=self.listing1,
            user=self.user1,
            comment="Comment 1",
            time=datetime.datetime.now(),
        )
        self.comment2 = Comment.objects.create(
            item=self.listing1,
            user=self.user2,
            comment="Comment 2",
            time=datetime.datetime.now(),
        )

    def test_getComments(self):
        """Test getComments function"""
        retrieved_comments = getComments(self.listing1)
        self.assertQuerySetEqual(retrieved_comments, [self.comment2, self.comment1])

    # Check for a listing without comments
    def test_no_comments(self):
        retrieved_comments = getComments(self.listing2)
        self.assertQuerySetEqual(retrieved_comments, [])


class GetCategoryListTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            id=1,
            username="user1",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.user2 = User.objects.create_user(
            id=2,
            username="user2",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.listing1 = Listing.objects.create(
            id=1,
            user_id=1,
            item="AAA",
            description="Description 1",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.listing2 = Listing.objects.create(
            id=2,
            user_id=2,
            item="BBB",
            description="Description 2",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="elec",
            active=True,
            number_of_bids=1,
        )

        self.listing3 = Listing.objects.create(
            id=3,
            user_id=1,
            item="ABC",
            description="Description 3",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.categoryArt1 = Category.objects.create(
            category_name="art", item=self.listing1
        )

        self.categoryArt2 = Category.objects.create(
            category_name="art", item=self.listing3
        )

        self.categoryElec1 = Category.objects.create(
            category_name="elec", item=self.listing2
        )

    def test_getCategoryList_1(self):
        """Test the getCategoryList function for art category"""
        results = getCategoryList("art")
        self.assertQuerySetEqual(results, [self.categoryArt1, self.categoryArt2])

    def test_getCategoryList_2(self):
        """Test the getCategoryList function for elec category"""
        results = getCategoryList("elec")
        self.assertQuerySetEqual(results, [self.categoryElec1])

    def test_getCategoryList_no_listings_in_category(self):
        """Test the getCategoryList function for category without listings"""
        results = getCategoryList("cars")
        self.assertQuerySetEqual(results, [])

    def test_getCategoryList_inexistent_category(self):
        """Test the getCategoryList function for category that doesn't exist"""
        results = getCategoryList("aaa")
        self.assertQuerySetEqual(results, [])


class getSearchResultsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            id=1,
            username="user1",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.user2 = User.objects.create_user(
            id=2,
            username="user2",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.listing1 = Listing.objects.create(
            id=1,
            user_id=1,
            item="AAA",
            description="Description 1",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.listing2 = Listing.objects.create(
            id=2,
            user_id=2,
            item="BBB",
            description="Description 2",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.listing3 = Listing.objects.create(
            id=3,
            user_id=1,
            item="ABC",
            description="Description 3",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

    def test_getSearchResults_1letter(self):
        """Test the getSearchResults function"""
        results = getSearchResults("a", [self.listing1, self.listing2, self.listing3])
        self.assertListEqual(results, [self.listing1, self.listing3])

    def test_getSearchResults_anotherLetter(self):
        """Test the getSearchResults function"""
        results = getSearchResults("b", [self.listing1, self.listing2, self.listing3])
        self.assertListEqual(results, [self.listing2, self.listing3])

    def test_getSearchResults_exactWord(self):
        """Test the getSearchResults function"""
        results = getSearchResults("abc", [self.listing1, self.listing2, self.listing3])
        self.assertListEqual(results, [self.listing3])

    def test_getSearchResults_noResults(self):
        """Test the getSearchResults function"""
        results = getSearchResults("zzz", [self.listing1, self.listing2, self.listing3])
        self.assertListEqual(results, [])


# Tests for listing model
class calcMinBidTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            id=1,
            username="user1",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.user2 = User.objects.create_user(
            id=2,
            username="user2",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.listing1 = Listing.objects.create(
            id=1,
            user_id=1,
            item="AAA",
            description="Description 1",
            starting_bid=10,
            date=datetime.datetime.now(),
            current_price=0,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.listing2 = Listing.objects.create(
            id=2,
            user_id=2,
            item="BBB",
            description="Description 2",
            starting_bid=10,
            date=datetime.datetime.now(),
            current_price=15,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.listing3 = Listing.objects.create(
            id=3,
            user_id=1,
            item="ABC",
            description="Description 3",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )
    
    def test_calcMinBid(self):
        minBid1 = self.listing1.calcMinBid()
        minBid2 = self.listing2.calcMinBid()
        minBid3 = self.listing3.calcMinBid()

        self.assertEqual(minBid1, 11)
        self.assertEqual(minBid2, 16)
        self.assertEqual(minBid3, 3)

# Tests for views
class TestViews(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            id=1,
            username="user1",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.user2 = User.objects.create_user(
            id=2,
            username="user2",
            email="email",
            password="pass",
            first_name="firstname",
            last_name="lastname",
        )

        self.listing1 = Listing.objects.create(
            id=1,
            user_id=1,
            item="AAA",
            description="Description 1",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

        self.listing2 = Listing.objects.create(
            id=2,
            user_id=2,
            item="BBB",
            description="Description 2",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="elec",
            active=True,
            number_of_bids=1,
        )

        self.listing3 = Listing.objects.create(
            id=3,
            user_id=1,
            item="ABC",
            description="Description 3",
            starting_bid=1,
            date=datetime.datetime.now(),
            current_price=2,
            category="art",
            active=True,
            number_of_bids=1,
        )

    def test_index_view(self):
        # Set up client to make requests
        c = Client()

        # Send get request to index page and store response
        response = c.get("")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure three flights are returned in the context
        self.assertEqual(response.context["all_listings"].count(), 3)

    def test_listing_view(self):
        # Set up client to make requests
        c = Client()

        # Send get request to index page and store response
        response = c.get("/1")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

        # Try with a non-existing index
        max_id = Listing.objects.all().aggregate(Max("id"))["id__max"]

        response_invalid = c.get(f"/{max_id+1}")
        self.assertEqual(response_invalid.status_code, 404)

    def test_categories_view(self):
        pass



        