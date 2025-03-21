package com.cse327project.pitlessbucket.auth.presentation.sign_up

data class SignInResult(
    val data: UserData?,
    val errorMessage: String?
)

data class UserData(
    val userId: String,
    val username: String?,
    val profilePictureUrl: String?,
    val idToken: String?
)
