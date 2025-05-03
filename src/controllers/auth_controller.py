from flask import Blueprint, redirect, request, session, jsonify, current_app
from utils.github_oauth import get_access_token, get_user_info
from services.mongo_service import mongo_service
from models.user_activity_model import create_user_activity
from services.activity_service import log_user_activity
from datetime import datetime, timezone


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login/github")
def login_github():
    redirect_url = request.args.get("redirect", current_app.config["FRONTEND_URL"])
    session["redirect_after_login"] = redirect_url

    github_oauth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={current_app.config['GITHUB_CLIENT_ID']}&scope=user:email"
    )
    return redirect(github_oauth_url)


@auth_bp.route("/login/github/callback")
def github_callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    token = get_access_token(code)
    if not token:
        return "Failed to get access token", 400

    user_info = get_user_info(token)

    # Fallback email logic
    username = user_info.get("login")
    email = user_info.get("email") or f"{username}@users.noreply.github.com"

    if not username:
        current_app.logger.error("GitHub user info missing username")
        return "GitHub login failed", 400

    session["user"] = {
        "username": username,
        "email": email,
        "name": user_info.get("name"),
        "avatar": user_info.get("avatar_url")
    }
    session.modified = True

    current_app.logger.info(f"User info stored in session: {session['user']}")

    # Try to log user activity, but don't fail the login if it doesn't work
    try:
        current_app.logger.info("Attempting to log user signin activity...")

        # Check MongoDB initialization
        db_initialized = mongo_service.db is not None
        user_activity_initialized = mongo_service.user_activity is not None
        current_app.logger.info(f"MongoDB initialization status: db={db_initialized}, user_activity={user_activity_initialized}")

        # If MongoDB is not initialized, try to initialize it
        if not db_initialized or not user_activity_initialized:
            current_app.logger.info("MongoDB not fully initialized, attempting to initialize...")
            mongo_service.initialize()
            mongo_service.ensure_collections()

            # Check again
            db_initialized = mongo_service.db is not None
            user_activity_initialized = mongo_service.user_activity is not None
            current_app.logger.info(f"MongoDB initialization status after retry: {db_initialized}, {user_activity_initialized}")

        if db_initialized and user_activity_initialized:
            # Only use the log_user_activity function to avoid duplicate records
            current_app.logger.info("Logging signin activity...")
            success = log_user_activity(user_info, "signin")
            current_app.logger.info(f"Signin activity logging success: {success}")

            # Count documents in the collection
            count = mongo_service.user_activity.count_documents({})
            current_app.logger.info(f"Total documents in user_activity collection: {count}")
        else:
            current_app.logger.warning("MongoDB service not fully initialized, skipping activity logging")
            success = False
    except Exception as e:
        current_app.logger.error(f"Failed to log user activity: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())

    return redirect(session.pop("redirect_after_login", current_app.config["FRONTEND_URL"]))



@auth_bp.route("/me")
def get_me():
    if "user" not in session:
        current_app.logger.info("Session does not contain user")
        return jsonify({}), 401
    return jsonify(session["user"])

@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Print request details
    current_app.logger.info(f"Received logout request")
    current_app.logger.info(f"Request method: {request.method}")
    current_app.logger.info(f"Request headers: {dict(request.headers)}")

    user_data = session.get("user")
    current_app.logger.info(f"Logout requested. User data in session: {user_data}")

    if user_data:
        # Try direct MongoDB insert for logout activity
        current_app.logger.info("Attempting direct MongoDB insert for logout activity...")

        # Check MongoDB initialization
        db_initialized = mongo_service.db is not None
        user_activity_initialized = mongo_service.user_activity is not None
        current_app.logger.info(f"MongoDB initialization status: db={db_initialized}, user_activity={user_activity_initialized}")

        # If MongoDB is not initialized, try to initialize it
        if not db_initialized or not user_activity_initialized:
            current_app.logger.info("MongoDB not fully initialized, attempting to initialize...")
            mongo_service.initialize()
            mongo_service.ensure_collections()

            # Check again
            db_initialized = mongo_service.db is not None
            user_activity_initialized = mongo_service.user_activity is not None
            current_app.logger.info(f"MongoDB initialization status after retry: {db_initialized}, {user_activity_initialized}")

        if db_initialized and user_activity_initialized:
            try:
                # Only use the log_user_activity function to avoid duplicate records
                current_app.logger.info("Logging logout activity...")
                success = log_user_activity(user_data, "logout")
                current_app.logger.info(f"Logout activity logging success: {success}")

                # Count documents in the collection
                count = mongo_service.user_activity.count_documents({})
                current_app.logger.info(f"Total documents in user_activity collection after logout: {count}")

                session.clear()
                return jsonify({
                    "message": "Logged out",
                    "success": True,
                    "total_documents": count
                }), 200
            except Exception as e:
                current_app.logger.error(f"Error logging logout activity: {str(e)}")
                import traceback
                current_app.logger.error(traceback.format_exc())
                session.clear()
                return jsonify({
                    "message": "Logged out",
                    "success": False,
                    "error": str(e)
                }), 200
        else:
            current_app.logger.error("MongoDB not fully initialized for logout!")
            session.clear()
            return jsonify({
                "message": "Logged out",
                "success": False,
                "error": "MongoDB not fully initialized"
            }), 200
    else:
        current_app.logger.warning("No user data found in session for logout.")
        session.clear()
        return jsonify({
            "message": "Logged out",
            "success": False,
            "error": "No user data found in session"
        }), 200


@auth_bp.route("/test-login", methods=["POST"])
def test_login():
    """Test endpoint to simulate a login."""
    try:
        # Print request details
        current_app.logger.info(f"Received test login request")
        current_app.logger.info(f"Request method: {request.method}")
        current_app.logger.info(f"Request headers: {dict(request.headers)}")
        current_app.logger.info(f"Request data: {request.data}")

        # Get user data from request
        user_data = request.json
        if not user_data:
            current_app.logger.error("No JSON data in request")
            return jsonify({
                "success": False,
                "error": "No JSON data in request"
            }), 400

        current_app.logger.info(f"Test login with user data: {user_data}")

        # Store user in session
        session["user"] = user_data
        session.modified = True
        current_app.logger.info(f"User stored in session: {session.get('user')}")

        # Try direct MongoDB insert for login activity
        current_app.logger.info("Attempting direct MongoDB insert for login activity...")

        # Check MongoDB initialization
        db_initialized = mongo_service.db is not None
        user_activity_initialized = mongo_service.user_activity is not None
        current_app.logger.info(f"MongoDB initialization status: db={db_initialized}, user_activity={user_activity_initialized}")

        # If MongoDB is not initialized, try to initialize it
        if not db_initialized or not user_activity_initialized:
            current_app.logger.info("MongoDB not fully initialized, attempting to initialize...")
            mongo_service.initialize()
            mongo_service.ensure_collections()

            # Check again
            db_initialized = mongo_service.db is not None
            user_activity_initialized = mongo_service.user_activity is not None
            current_app.logger.info(f"MongoDB initialization status after retry: {db_initialized}, {user_activity_initialized}")

        if db_initialized and user_activity_initialized:
            # Only use the log_user_activity function to avoid duplicate records
            current_app.logger.info("Logging test signin activity...")
            success = log_user_activity(user_data, "signin")
            current_app.logger.info(f"Test login activity logging success: {success}")

            # Count documents in the collection
            count = mongo_service.user_activity.count_documents({})
            current_app.logger.info(f"Total documents in user_activity collection: {count}")

            return jsonify({
                "success": True,
                "message": "Test login successful",
                "user": user_data,
                "service_result": success,
                "total_documents": count
            }), 200
        else:
            current_app.logger.error("MongoDB not fully initialized!")
            return jsonify({
                "success": False,
                "message": "MongoDB not fully initialized",
                "user": user_data
            }), 500

    except Exception as e:
        current_app.logger.error(f"Test login failed: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@auth_bp.route("/admin/clear-activity-logs", methods=["POST"])
def clear_activity_logs():
    """Admin endpoint to clear all activity logs."""
    try:
        # Check if user is admin (you should implement proper authentication)
        # For now, we'll just check if the request is from localhost
        if request.remote_addr not in ['127.0.0.1', 'localhost']:
            return jsonify({
                "success": False,
                "error": "Unauthorized"
            }), 403

        # Check MongoDB initialization
        db_initialized = mongo_service.db is not None
        user_activity_initialized = mongo_service.user_activity is not None

        if db_initialized and user_activity_initialized:
            # Count documents before deletion
            count_before = mongo_service.user_activity.count_documents({})

            # Delete all documents
            result = mongo_service.user_activity.delete_many({})

            # Verify collection is empty
            count_after = mongo_service.user_activity.count_documents({})

            return jsonify({
                "success": True,
                "deleted_count": result.deleted_count,
                "count_before": count_before,
                "count_after": count_after
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "MongoDB not fully initialized"
            }), 500

    except Exception as e:
        current_app.logger.error(f"Failed to clear activity logs: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@auth_bp.route("/debug-mongo", methods=["GET"])
def debug_mongo():
    """Debug endpoint to check MongoDB connection."""
    try:
        # Check MongoDB initialization
        db_initialized = mongo_service.db is not None
        user_activity_initialized = mongo_service.user_activity is not None

        # If MongoDB is not initialized, try to initialize it
        if not db_initialized or not user_activity_initialized:
            current_app.logger.info("MongoDB not fully initialized, attempting to initialize...")
            mongo_service.initialize()
            mongo_service.ensure_collections()

            # Check again
            db_initialized = mongo_service.db is not None
            user_activity_initialized = mongo_service.user_activity is not None

        # Try to insert a test document
        if db_initialized and user_activity_initialized:
            test_doc = {
                "test": True,
                "timestamp": datetime.now(timezone.utc)
            }
            result = mongo_service.user_activity.insert_one(test_doc)

            # Get all collections
            collections = mongo_service.db.list_collection_names()

            # Count documents in user_activity
            count = mongo_service.user_activity.count_documents({})

            # Get recent documents
            recent_docs = list(mongo_service.user_activity.find().sort("timestamp", -1).limit(5))
            recent_docs_str = []
            for doc in recent_docs:
                doc_copy = doc.copy()
                doc_copy["_id"] = str(doc_copy["_id"])
                if "timestamp" in doc_copy and isinstance(doc_copy["timestamp"], datetime):
                    doc_copy["timestamp"] = doc_copy["timestamp"].isoformat()
                recent_docs_str.append(doc_copy)

            return jsonify({
                "success": True,
                "mongo_initialized": {
                    "db": db_initialized,
                    "user_activity": user_activity_initialized
                },
                "test_insert_id": str(result.inserted_id),
                "collections": collections,
                "user_activity_count": count,
                "recent_documents": recent_docs_str
            }), 200
        else:
            return jsonify({
                "success": False,
                "mongo_initialized": {
                    "db": db_initialized,
                    "user_activity": user_activity_initialized
                },
                "error": "MongoDB not fully initialized"
            }), 500

    except Exception as e:
        current_app.logger.error(f"Debug MongoDB failed: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@auth_bp.route("/test-activity-log", methods=["GET"])
def test_activity_log():
    """Test endpoint to directly log activity to MongoDB."""
    try:
        # Check MongoDB initialization
        db_initialized = mongo_service.db is not None
        user_activity_initialized = mongo_service.user_activity is not None
        mongo_initialized = {
            "db": db_initialized,
            "user_activity": user_activity_initialized
        }
        current_app.logger.info(f"MongoDB initialization status: {mongo_initialized}")

        # If MongoDB is not initialized, try to initialize it
        if not db_initialized or not user_activity_initialized:
            current_app.logger.info("MongoDB not fully initialized, attempting to initialize...")
            mongo_service.initialize()
            mongo_service.ensure_collections()

            # Check again
            db_initialized = mongo_service.db is not None
            user_activity_initialized = mongo_service.user_activity is not None
            mongo_initialized = {
                "db": db_initialized,
                "user_activity": user_activity_initialized
            }
            current_app.logger.info(f"MongoDB initialization status after retry: {mongo_initialized}")

        # Create a test user
        test_user = {
            "username": "test_user",
            "email": "test@example.com",
            "name": "Test User",
            "avatar": "https://example.com/avatar.png"
        }

        # Try direct MongoDB access
        if db_initialized and user_activity_initialized:
            # Method 1: Direct insert using mongo_service
            activity_data = create_user_activity(test_user, "test_direct")
            current_app.logger.info(f"Activity data to be inserted directly: {activity_data}")

            direct_result = mongo_service.user_activity.insert_one(activity_data)
            current_app.logger.info(f"Direct insert result ID: {direct_result.inserted_id}")

            # Method 2: Using log_user_activity function
            service_result = log_user_activity(test_user, "test_service")
            current_app.logger.info(f"Service logging result: {service_result}")

            # Count documents in the collection
            count = mongo_service.user_activity.count_documents({})

            return jsonify({
                "success": True,
                "mongo_initialized": mongo_initialized,
                "direct_insert_id": str(direct_result.inserted_id),
                "service_result": service_result,
                "total_documents": count
            }), 200
        else:
            return jsonify({
                "success": False,
                "mongo_initialized": mongo_initialized,
                "error": "MongoDB service not fully initialized"
            }), 500

    except Exception as e:
        current_app.logger.error(f"Test activity log failed: {str(e)}")
        import traceback
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

