class CreateUsers < ActiveRecord::Migration[5.0]
  def change
    create_table :users do |t|
      t.string :name
      t.string :email
      t.string :password_digest
      t.string :contact_number
      t.integer :gender
      t.integer :age
      t.string :authentication_token

      t.timestamps
    end
  end
end
