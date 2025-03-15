package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard

import okhttp3.MultipartBody
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface ApiService {
    @GET("/api/v1/file_manager/list_files")
    suspend fun getFiles(@Header("Authorization") authHeader: String): List<FileInfo>

    @Multipart
    @POST("/api/v1/file_manager/upload_file")
    suspend fun uploadFile(
        @Header("Authorization") token: String,
        @Part file: MultipartBody.Part
    ): Response<UploadResponse>
}
data class UploadResponse(
    val message: String,
    val filename: String
)