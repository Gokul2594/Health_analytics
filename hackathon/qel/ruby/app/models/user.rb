class User < ApplicationRecord
  has_secure_password
	enum gender: [:male, :female]
	validates :name, :email, presence: true
	validates :name, :email, uniqueness: true
	before_save :create_authentication_token

	private
	def create_authentication_token
		self.authentication_token=SecureRandom.urlsafe_base64
	end
end
