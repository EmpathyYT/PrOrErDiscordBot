import discord
import os
from dotenv import load_dotenv

load_dotenv()

bug_users_table = 'BugUsers'
bug_reports_table = 'BugReports'
feature_requests_table = 'SuggestionReports'
feature_users_table = 'SuggestionUsers'
id_field_name = 'id'
bug_report_id_field_name = 'bug_report_id'
feature_request_id_field_name = 'suggestion_id'
message_id_field_name = 'message_id'
created_at_field_name = 'created_at'
closed_alpha_field_name = 'closed_alpha'
user_id_field_name = 'user_id'
submittal_confirmation_channel = discord.Object(id=1374477393800073337)
feature_request_channel = discord.Object(id=1374432042988732578)
version_tracker_channel = discord.Object(id=1384565719953571892)
testing_channel = discord.Object(id=1374399824392224909)
open_updates_channel = discord.Object(id=1367019660142448674)
closed_updates_channel = discord.Object(id=1408122777722032158)
open_bug_report_channel = discord.Object(id=1374419412924371065)
closed_bug_report_channel = discord.Object(id=1408122828561191044)
guild = discord.Object(id=os.getenv('GUILD_ID')) # type: ignore
app_tester_role = discord.Object(id=1373542685243080704)
closed_tester_role = discord.Object(id=1385713445248176168)
app_dev_role = discord.Object(id=1373543360572162048)
to_do_channel = discord.Object(id=1375076079156592640)
to_do_seperator = "<-------->"



# todo change this before pushing
is_testing = False
