import time
import flask

app = flask.Flask(__name__)

@app.route('/time')
def get_current_time():
    return {'time': time.strftime('%a, %B %d, %Y %I:%M:%S')}

@app.route('/')
def home():
    return 'Hello World!'
# @app.route('/')
# @app.route('/<path:filename>')
# def dashboard(filename):
#     return flask.send_from_directory('./src/views/Dashboard', filename)
# const dashboardRoutes = [
#   {
#     path: "/dashboard",
#     name: "Dashboard",
#     rtlName: "لوحة القيادة",
#     icon: Dashboard,
#     component: DashboardPage,
#     layout: "/admin"
#   },
#   {
#     path: "/user",
#     name: "User Profile",
#     rtlName: "ملف تعريفي للمستخدم",
#     icon: Person,
#     component: UserProfile,
#     layout: "/admin"
#   },
#   {
#     path: "/table",
#     name: "Table List",
#     rtlName: "قائمة الجدول",
#     icon: "content_paste",
#     component: TableList,
#     layout: "/admin"
#   },
#   {
#     path: "/typography",
#     name: "Typography",
#     rtlName: "طباعة",
#     icon: LibraryBooks,
#     component: Typography,
#     layout: "/admin"
#   },
#   {
#     path: "/icons",
#     name: "Icons",
#     rtlName: "الرموز",
#     icon: BubbleChart,
#     component: Icons,
#     layout: "/admin"
#   },
#   {
#     path: "/maps",
#     name: "Maps",
#     rtlName: "خرائط",
#     icon: LocationOn,
#     component: Maps,
#     layout: "/admin"
#   },
#   {
#     path: "/notifications",
#     name: "Notifications",
#     rtlName: "إخطارات",
#     icon: Notifications,
#     component: NotificationsPage,
#     layout: "/admin"
#   },
#   {
#     path: "/rtl-page",
#     name: "RTL Support",
#     rtlName: "پشتیبانی از راست به چپ",
#     icon: Language,
#     component: RTLPage,
#     layout: "/rtl"
#   },
#   {
#     path: "/upgrade-to-pro",
#     name: "Upgrade To PRO",
#     rtlName: "التطور للاحترافية",
#     icon: Unarchive,
#     component: UpgradeToPro,
#     layout: "/admin"
#   }
# ];