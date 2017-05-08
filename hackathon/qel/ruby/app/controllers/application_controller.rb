class ApplicationController < ActionController::Base
	include SessionsHelper
  protect_from_forgery with: :null_session
end
