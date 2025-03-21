package com.cse327project.pitlessbucket.core.data.data_source

import com.cse327project.pitlessbucket.file_manager.domain.model.FileInfo
import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part
import retrofit2.http.Query

interface ApiService {
    @GET("/api/v1/file_manager/list_files")
    suspend fun getFiles(@Header("Authorization") authHeader: String): List<FileInfo>

    @Multipart
    @POST("/api/v1/file_manager/upload_file")
    suspend fun uploadFile(
        @Header("Authorization") token: String,
        @Part file: MultipartBody.Part
    ): Response<UploadResponse>

    @GET("/api/download")
    suspend fun downloadFile(
        @Query("file_id") fileId: String,
        @Header("Authorization") token: String
    ): Response<ResponseBody>
}
data class UploadResponse(
    val message: String,
    val filename: String
)