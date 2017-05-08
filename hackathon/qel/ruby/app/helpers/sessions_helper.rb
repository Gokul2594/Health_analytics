module SessionsHelper
  def current_user
    @current_user ||= User.find_by(authentication_token: request.headers['Access-Token'])
  end
end