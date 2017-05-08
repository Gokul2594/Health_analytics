class UsersController < ApplicationController
  require 'uri'
  require 'net/http'
  require 'json'
  before_action :set_user, only: [:show, :edit, :update, :destroy]

  # GET /users
  # GET /users.json
  def index
    @users = User.all
  end

  # GET /users/1
  # GET /users/1.json
  def show
  end

  # GET /users/new
  def new
    @user = User.new
  end

  # GET /users/1/edit
  def edit
  end

  # POST /users
  # POST /users.json
  def create
    @user = User.new(user_params)

    respond_to do |format|
      if @user.save
        format.html { redirect_to complete_test_path, notice: 'User was successfully created.' }
        format.json { render :show, status: :created, location: @user }
      else
        format.html { render :new }
        format.json { render json: @user.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /users/1
  # PATCH/PUT /users/1.json
  def update
    respond_to do |format|
      if @user.update(user_params)
        format.html { redirect_to @user, notice: 'User was successfully updated.' }
        format.json { render :show, status: :ok, location: @user }
      else
        format.html { render :edit }
        format.json { render json: @user.errors, status: :unprocessable_entity }
      end
    end
  end

  def login_new
  end

  def login
    respond_to do |format|
      user=User.find_by_email(params[:email])
      if user && user.authenticate(params[:password])
        format.html { redirect_to complete_test_path, notice: 'User was successfully updated.' }
      else
        format.html { render :login_new }
      end
    end
  end

  def complete_test
  end

  def create_complete_test
    data = []
    hemo_data = {}
    hemo_data["hemoglobin"] = params[:complete_test][:hemoglobin]
    hemo_data["pcv"] = params[:complete_test][:pcv]
    hemo_data["rbc"] = params[:complete_test][:rbc]
    hemo_data["mchc"] = params[:complete_test][:mchc]
    hemo_data["mcv"] = params[:complete_test][:mcv]
    hemo_data["mch"] = params[:complete_test][:mch]
    hemo_data["esr"] = params[:complete_test][:esr]
    hemo_data["plateles_count"] = params[:complete_test][:plateles_count]
    hemo_data["sex"] = 'male'
    data << hemo_data
    bio_chemical = {}
    bio_chemical["fbs/ppbs"] = params[:complete_test][:fbs_ppbs]
    bio_chemical["blood_urea"] = params[:complete_test][:blood_urea]
    bio_chemical["creatinine"] = params[:complete_test][:creatinine]
    bio_chemical["uric_acid"] = params[:complete_test][:uric_acid]
    bio_chemical["sex"] = 'male'
    data << bio_chemical
    lipid = {}
    lipid["total_cholesterol"] = params[:complete_test][:total_cholesterol]
    lipid["hdl_cholesterol"] = params[:complete_test][:hdl_cholesterol]
    lipid["ldl_cholesterol"] = params[:complete_test][:idl_cholesterol]
    lipid["triglycerides"] = params[:complete_test][:triglycerides]
    lipid["total_cholesterol/hdl_ratio"] = params[:complete_test][:total_cholesterol_hdl_ratio]
    data << lipid
    liver_function = {}
    liver_function["total_protein"]
    liver_function["albumin"] = params[:complete_test][:albumin]
    liver_function["globulin"] = params[:complete_test][:globulin]
    liver_function["a/g_ratio"] = params[:complete_test][:a_g_ratio]
    liver_function["sgot"] = params[:complete_test][:sgot]
    liver_function["sgpt"] = params[:complete_test][:sgpt]
    liver_function["alkaline_phosphate"] = params[:complete_test][:alkaline_phosphate]
    liver_function["bilirubin_total"] = params[:complete_test][:bilirubin_total]
    liver_function["bilirubin_direct"] = params[:complete_test][:bilirubin_direct]
    liver_function["gamma_gt"] = params[:complete_test][:gamma_gt]
    data << liver_function

    input = {}
    params = {}
    params[:data] = data
    input[:params] = params

    url = URI("http://139.59.70.171:8069/health/complete_test")
    http = Net::HTTP.new(url.host, url.port)
    request = Net::HTTP::Post.new(url)
    request["content-type"] = 'application/json'
    request["cache-control"] = 'no-cache'
    request.body = input.to_json
    response = http.request(request)
    parsed_data = JSON.load(response.body)
    parsed_result = JSON.load(parsed_data["result"])
    lipid = parsed_result["lipid_result"]["predictions"]
    hemogram = parsed_result["hemo_result"]["predictions"]
    liver_func_result = parsed_result["liver_func_result"]["predictions"]
    bio_chemical = parsed_result["bio_chemical_result"]["predictions"]

    # flash[:lipid] = lipid
    # flash[:hemogram] = hemogram
    # flash[:liver_func_result] = liver_func_result
    # flash[:bio_chemical] = bio_chemical
    # binding.pry

    redirect_to "/display_result/#{hemogram}/#{bio_chemical}/#{lipid}/#{liver_func_result}", overwrite: {hemogram: hemogram, bio: bio_chemical, lipid: lipid, liver: liver_func_result}

  end

  def display_result
  end

  # DELETE /users/1
  # DELETE /users/1.json
  def destroy
    @user.destroy
    respond_to do |format|
      format.html { redirect_to users_url, notice: 'User was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_user
      @user = User.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def user_params
      params.require(:user).permit(:name, :email, :password, :contact_number, :gender, :age)
    end

    def complete_test_params
      params.require(:complete_test).permit(:hemoglobin, :pcv, :rbc, :mchc, :mcv, :mch, :esr, :plateles_count, :fbs_ppbs, :blood_urea, :creatinine, :uric_acid, :total_cholesterol, :hdl_cholesterol, :idl_cholesterol, :triglycerides, :total_cholesterol_hdl_ratio, :total_protein, :albumin, :globulin, :a_g_ratio, :sgot, :sgpt, :alkaline_phosphate, :bilirubin_total, :bilirubin_direct, :gamma_gt)
    end
end
