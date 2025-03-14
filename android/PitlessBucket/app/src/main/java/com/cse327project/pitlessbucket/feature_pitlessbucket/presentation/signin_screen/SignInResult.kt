package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen

data class SignInResult(
    val data: UserData?,
    val errorMessage: String?
)

data class UserData(
    val userId: String,
    val username: String?,
    val profilePictureUrl: String?
)
